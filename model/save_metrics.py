import pandas as pd
import json
import joblib
import time
import string, re
from core.config import settings
from sklearn.preprocessing import label_binarize
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

print("Carregando modelo e encoder")

start = time.time()

model = joblib.load(settings.MODEL_PATH)
label_encoder = joblib.load(settings.ENCODER_PATH)

print("Carregando amostra do dataset")

df = pd.read_csv(settings.DATASET_PATH)

suspicious_keywords = ['login','signin','verify','update','banking','account','secure','ebay','paypal']

def extract_features(url):
    features = {}
    features['url_length'] = len(url)
    features['num_digits'] = sum(c.isdigit() for c in url)
    features['num_special_chars'] = sum(c in string.punctuation for c in url)
    features['num_subdomains'] = url.count('.') - 1
    features['has_ip'] = int(bool(re.search(r'\d+\.\d+\.\d+\.\d+', url)))
    features['has_https'] = int('https' in url.lower())
    features['num_params'] = url.count('?')
    features['num_fragments'] = url.count('#')
    features['num_slashes'] = url.count('/')
    features['has_suspicious_words'] = int(any(word in url.lower() for word in suspicious_keywords))
    tld = url.split('.')[-1]
    features['tld_length'] = len(tld)
    features['is_common_tld'] = int(tld in ['com','org','net','edu','gov'])
    features['has_hex'] = int(bool(re.search(r'%[0-9a-fA-F]{2}', url)))
    features['repeated_chars'] = int(bool(re.search(r'(.)\1{3,}', url)))
    return pd.Series(features)

print("Extraindo features e calculando métricas")

X = df['url'].apply(extract_features)
y_true = label_encoder.transform(df['type'])
y_pred = model.predict(X)

y_true_bin = label_binarize(y_true, classes=range(len(model.classes_)))
y_proba = model.predict_proba(X)

metrics = {
    "accuracy": accuracy_score(y_true, y_pred),
    "precision": precision_score(y_true, y_pred, average="weighted"),
    "recall": recall_score(y_true, y_pred, average="weighted"),
    "f1_score": f1_score(y_true, y_pred, average="weighted"),
    "roc_auc": roc_auc_score(y_true_bin, y_proba, average="weighted", multi_class="ovr")
}

metrics["confusion_matrix"] = confusion_matrix(y_true, y_pred).tolist()

print("Salvando métricas")

with open(settings.METRICS_PATH, "w") as f:
    json.dump(metrics, f, indent=4)

y_pred = model.predict(X)

print(f"Tempo de predição: {time.time() - start:.2f} segundos")

print("✅ Métricas salvas com sucesso ✅")