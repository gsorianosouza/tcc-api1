import pandas as pd
import json
import joblib
import time
import string, re
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix



print("Carregando modelo e encoder...")
model = joblib.load("C:/Users/gabri/Desktop/tcc2/tcc-api/tcc-api/model/rf_model.pkl")
label_encoder = joblib.load("C:/Users/gabri/Desktop/tcc2/tcc-api/tcc-api/model/label_encoder.pkl")

print("Carregando amostra do dataset...")
df = pd.read_csv("C:/Users/gabri/Desktop/tcc2/tcc-api/tcc-api/model/dataset/malicious_phish.csv")

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

print("Extraindo features e calculando métricas...")
X = df['url'].apply(extract_features)
y_true = label_encoder.transform(df['type'])
y_pred = model.predict(X)
y_proba = model.predict_proba(X)[:, 1] if len(model.classes_) == 2 else None

metrics = {
    "accuracy": accuracy_score(y_true, y_pred),
    "precision": precision_score(y_true, y_pred, average="weighted"),
    "recall": recall_score(y_true, y_pred, average="weighted"),
    "f1_score": f1_score(y_true, y_pred, average="weighted"),
}

if y_proba is not None:
    from sklearn.metrics import roc_auc_score
    metrics["roc_auc"] = roc_auc_score(y_true, y_proba)

metrics["confusion_matrix"] = confusion_matrix(y_true, y_pred).tolist()

print("Salvando métricas...")
with open("C:/Users/gabri/Desktop/tcc2/tcc-api/tcc-api/model/metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

start = time.time()
y_pred = model.predict(X)  # ou X_test
print(f"Tempo de predição: {time.time() - start:.2f} segundos")

print("✅ Métricas salvas com sucesso")