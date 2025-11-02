from fastapi import HTTPException
from ml.model.model_manager_loader import model_manager
from ml.models.prediction import Prediction
from sqlalchemy.orm import Session
from ml.schemas.ml import PredictionSchema
from ml.utils.ml_utils import is_valid_url, extract_features, check_url_status

load_model = model_manager

def get_predictions(db: Session):
    return db.query(Prediction).all()

def make_prediction(url: str, db: Session):
    is_url = url.strip()
    
    if not is_valid_url(is_url):
        raise HTTPException(status_code=400, detail="URL inválida.")
    
    features = extract_features(url)
    url_status = check_url_status(url)
    
    prob_dict = {}
    result_label = None
    confidence = None
    
    model = load_model.model
    encoder = load_model.encoder
    
    if model is None or encoder is None:
        raise HTTPException(
            status_code=400,
            detail="Nenhum modelo treinado disponível. Por favor, use a rota de treinamento para treinar o modelo antes de fazer previsões."
        )
        
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(features)[0] 
        prob_dict = dict(zip(encoder.classes_, map(float, probs)))

        phishing_class = "phishing"
        phishing_prob = prob_dict.get(phishing_class, 0.0)
        result_label = "phishing" if phishing_prob >= 0.5 else "benign"

        confidence = max(prob_dict.values())
    else:
        pred_label_encoded = model.predict(features)[0]
        pred_label = encoder.inverse_transform([pred_label_encoded])[0]

        result_label = pred_label
        prob_dict = {cls: None for cls in encoder.classes_}

    prob_dict['url_status_code'] = url_status

    new_prediction = Prediction(input_text=url, result=result_label)
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)
    
    return PredictionSchema(
        url=url,
        prediction=result_label,
        confidence=confidence,
        probabilities=prob_dict,   
        prediction_id=new_prediction.id
    )
    
    