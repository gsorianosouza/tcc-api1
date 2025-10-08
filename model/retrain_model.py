import pandas as pd
import joblib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Prediction, Feedback
from core.config import settings
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

engine = create_engine(settings.DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def feature_engineering(urls):
    import string, re
    from urllib.parse import urlparse
    suspicious_keywords = ['login','signin','verify','update','banking','account','secure','ebay','paypal']

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

def retrain_model():
    feedbacked = session.query(Prediction).join(Feedback, Prediction.id==Feedback.prediction_id).all()
    if not feedbacked:
        print("Nenhum dado com feedback disponível para retreinamento.")
        return

    urls = []
    labels = []

    for p in feedbacked:
        for fb in p.feedbacks:
            urls.append(p.input_text)
            labels.append(fb.correct_label)

    X = feature_engineering(urls)
    le = LabelEncoder()
    y = le.fit_transform(labels)

    model = RandomForestClassifier(n_estimators=200, max_depth=15,random_state=42)
    model.fit(X, y)

    joblib.dump(model, settings.MODEL_PATH)
    joblib.dump(le, settings.ENCODER_PATH)

    print("Modelo retreinado com sucesso!")

if __name__ == "__main__":
    retrain_model()
    session.close()