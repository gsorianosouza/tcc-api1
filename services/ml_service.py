import re
import string
import joblib
import pandas as pd
from urllib.parse import urlparse
from fastapi import HTTPException
from sqlalchemy.orm import Session
import requests 
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects, RequestException

from db.models import Prediction, Feedback
from views.schemas.prediction_schema import PredictionRequest, PredictionResponse
from views.schemas.feedback_schema import FeedbackRequest, FeedbackResponse

model = joblib.load('./model/rf_model.pkl')
label_encoder = joblib.load('./model/label_encoder.pkl')

suspicious_keywords = ['login','signin','verify','update','banking','account','secure','ebay','paypal']

def check_url_status(url: str) -> int:

    test_url = url if '://' in url else 'http://' + url
    
    TIMEOUT = 5 
    
    try:
        response = requests.head(test_url, timeout=TIMEOUT, allow_redirects=True)
        
        if response.status_code == 200:
            return 1
        return -1
        
    except (ConnectionError, Timeout, TooManyRedirects):
        return 0
    except RequestException:
        return 0
    except Exception:
        return 0

def extract_features(url: str) -> pd.DataFrame:
    features = {}
    
    safe_url = url if '://' in url else 'http://' + url
    
    try:
        parsed_url = urlparse(safe_url)
        netloc = parsed_url.netloc
        tld = netloc.split('.')[-1]
    except Exception:
        tld = ''
        netloc = ''
        parsed_url = urlparse('')
    
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
    features['is_live'] = check_url_status(url)
    
    return pd.DataFrame([features])

def is_valid_url(url: str) -> bool:
    try:
        test_url = url if '://' in url else 'http://' + url
        result = urlparse(test_url)
        return all([result.scheme, result.netloc])
    except:
        return False

class MlService:

    @staticmethod
    def predict(payload: PredictionRequest, db: Session) -> PredictionResponse:
        url = payload.url.strip()

        if not is_valid_url(url):
            raise HTTPException(status_code=400, detail="Invalid URL format")

        features = extract_features(url)

        pred_label_encoded = model.predict(features)[0]
        pred_label = label_encoder.inverse_transform([pred_label_encoded])[0]

        url_status = check_url_status(url)
        
        if url_status == 0:
             pass

        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(features)[0]
            prob_dict = dict(zip(label_encoder.classes_, map(float, probs)))
        else:
            prob_dict = {cls: None for cls in label_encoder.classes_}

        new_prediction = Prediction(input_text=url, result=pred_label)
        db.add(new_prediction)
        db.commit()
        db.refresh(new_prediction)
        
        prob_dict['url_status_code'] = url_status
        return PredictionResponse(
            url=url,
            prediction=pred_label,
            probabilities=prob_dict,
            prediction_id=new_prediction.id
        )

    @staticmethod
    def feedback(payload: FeedbackRequest, db: Session) -> FeedbackResponse:
        prediction = db.query(Prediction).filter_by(id=payload.prediction_id).first()

        if not prediction:
            raise HTTPException(status_code=404, detail="Prediction not found!")

        existing_feedback = db.query(Feedback).filter_by(prediction_id=payload.prediction_id).first()
        if existing_feedback:
            raise HTTPException(status_code=400, detail="Feedback already exists for this prediction.")

        new_feedback = Feedback(
            prediction_id=payload.prediction_id,
            correct_label=payload.correct_label
        )
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)

        return FeedbackResponse(message="Feedback received successfully!")

ml_service = MlService()