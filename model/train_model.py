import pandas as pd
import numpy as np
import string
import re
import joblib
import requests 
from core.config import settings
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects, RequestException
from urllib.parse import urlparse
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv(settings.DATASET_PATH)

label_encoder = LabelEncoder()
df['label_encoded'] = label_encoder.fit_transform(df['type'])

suspicious_keywords = ['login','signin','verify','update','banking','account','secure','ebay','paypal']

def check_url_status(url: str) -> int:

    # Adiciona 'http://' se estiver faltando, para que requests tente se conectar
    test_url = url if '://' in url else 'http://' + url
    TIMEOUT = 5
    
    try:
        response = requests.head(test_url, timeout=TIMEOUT, allow_redirects=True)
        
        if 200 <= response.status_code < 400:
            return 1
        else:
            return -1
            
    except (ConnectionError, Timeout, TooManyRedirects, RequestException):
        return 0
    except Exception:
        return 0


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

print("Extraindo features (incluindo checagem de conectividade)...")
X = df['url'].apply(extract_features)
y = df['label_encoded']

print("Treinando o modelo RandomForest...")
model = RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42)
model.fit(X, y)

joblib.dump(model, settings.MODEL_PATH)
joblib.dump(label_encoder, settings.ENCODER_PATH)

print("Modelo e encoder salvos com sucesso!")