import pandas as pd
import json
import joblib
import time
import string
import re
from urllib.parse import urlparse
from core.config import settings
from sklearn.preprocessing import label_binarize
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from db.models import Prediction, Feedback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

suspicious_keywords = ['login','signin','verify','update','banking','account','secure','ebay','paypal']

def feature_engineering(urls):
    features_list = []
    for url in urls:
        features = {}
        safe_url = url if url.startswith(("http://","https://")) else 'http://' + url
        parsed_url = urlparse(safe_url)
        netloc = parsed_url.netloc
        tld = netloc.split('.')[-1] if netloc else ''
        features['url_length'] = len(url)
        features['num_digits'] = sum(c.isdigit() for c in url)
        features['num_special_chars'] = sum(c in string.punctuation for c in url)
        features['num_subdomains'] = netloc.count('.') - 1 if netloc else 0
        features['has_ip'] = int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', netloc)))
        features['has_https'] = int(parsed_url.scheme == 'https')
        features['num_params'] = url.count('?')
        features['num_fragments'] = url.count('#')
        features['num_slashes'] = url.count('/')
        features['has_suspicious_words'] = int(any(word in url.lower() for word in suspicious_keywords))
        features['tld_length'] = len(tld)
        features['is_common_tld'] = int(tld in ['com','org','net','edu','gov'])
        features['has_hex'] = int(bool(re.search(r'%[0-9a-fA-F]{2}', url)))
        features['repeated_chars'] = int(bool(re.search(r'(.)\1{3,}', url)))
        features_list.append(features)
    return pd.DataFrame(features_list)

print("Carregando modelo e encoder")
start = time.time()
model = joblib.load(settings.MODEL_PATH)
label_encoder = joblib.load(settings.ENCODER_PATH)

print("Carregando dataset original")
df = pd.read_csv(settings.DATASET_PATH)

feedbacked = session.query(Prediction).join(Feedback, Prediction.id==Feedback.prediction_id).all()

urls_feedback = []
labels_feedback = []

for p in feedbacked:
    for fb in p.feedbacks:
        urls_feedback.append(p.input_text)
        labels_feedback.append(fb.correct_label)

if urls_feedback:
    df_feedback = pd.DataFrame({'url': urls_feedback, 'type': labels_feedback})
    df = pd.concat([df, df_feedback], ignore_index=True)
    print(f"Adicionados {len(urls_feedback)} feedbacks ao dataset para métricas.")

print("Extraindo features...")
X = feature_engineering(df['url'])
y_true = label_encoder.transform(df['type'])

print("Calculando predições e métricas...")
y_pred = model.predict(X)
y_true_bin = label_binarize(y_true, classes=range(len(model.classes_)))
y_proba = model.predict_proba(X)

metrics = {
    "accuracy": accuracy_score(y_true, y_pred),
    "precision": precision_score(y_true, y_pred, average="weighted"),
    "recall": recall_score(y_true, y_pred, average="weighted"),
    "f1_score": f1_score(y_true, y_pred, average="weighted"),
    "roc_auc": roc_auc_score(y_true_bin, y_proba, average="weighted", multi_class="ovr"),
    "confusion_matrix": confusion_matrix(y_true, y_pred).tolist()
}

with open(settings.METRICS_PATH, "w") as f:
    json.dump(metrics, f, indent=4)

print(f"Tempo total de cálculo: {time.time() - start:.2f} segundos")
print("✅ Métricas atualizadas com sucesso ✅")

session.close()
