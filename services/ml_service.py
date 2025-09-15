from fastapi import HTTPException
import numpy as np
from core.config import settings
import joblib
from sqlalchemy.orm import Session
from db.models import Feedback, Model, Prediction
from views.schemas.feedback_schema import FeedbackRequest, FeedbackResponse
from views.schemas.prediction_schema import PredictionRequest, PredictionResponse, SSLDetails
import pandas as pd
from model.feature_extractor import extract_all_features, get_certificate_details, get_domain_from_url

model = joblib.load(settings.MODEL_PATH)

class MlService:
    
    @staticmethod
    def predict(payload: PredictionRequest, db: Session):
        if not payload.url.strip():
            raise HTTPException(status_code=400, detail="A URL não pode ser vazia")
        
        # OTIMIZAÇÃO: Extrai o domínio uma única vez no início
        domain = get_domain_from_url(payload.url)
        
        existing_prediction = db.query(Prediction).filter_by(input_text=payload.url).first()
        if existing_prediction:
            # CORRIGIDO: Recupere os detalhes do SSL para a resposta
            ssl_details_raw = get_certificate_details(domain)
            ssl_details_obj = SSLDetails(**ssl_details_raw) if ssl_details_raw else None
            
            return PredictionResponse(
                text=existing_prediction.input_text,
                prediction=existing_prediction.result,
                confidence_score=existing_prediction.confidence_score,
                prediction_id=existing_prediction.id,
                ssl_details=ssl_details_obj # Adicionado o detalhe SSL na resposta
            )
        
        # OTIMIZAÇÃO: O extrator já lida com falhas, então podemos chamar diretamente
        features = extract_all_features(payload.url)
        
        # OTIMIZAÇÃO: A variável confidence_score já existe, não precisa ser criada de novo
        df = pd.DataFrame([features])
        y_pred_proba = model.predict_proba(df)[0][1]
        y_pred = "Phishing" if y_pred_proba >= 0.5 else "Legítimo"
        
        # OTIMIZAÇÃO: Extrai os detalhes do SSL e cria o objeto para a resposta
        ssl_details_raw = get_certificate_details(domain)
        ssl_details_obj = SSLDetails(**ssl_details_raw) if ssl_details_raw else None

        model_record = db.query(Model).filter_by(name="XGBoostClassifier", version="1.0").first()
        if not model_record:
            model_record = Model(name="XGBoostClassifier", version="1.0")
            db.add(model_record)
            db.commit()
            db.refresh(model_record)

        new_prediction = Prediction(
            input_text=payload.url,
            result=y_pred,
            confidence_score = float(y_pred_proba),
            model_id=model_record.id
        )
        
        try:
            db.add(new_prediction)
            db.commit()
            db.refresh(new_prediction)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao salvar a previsão: {e}")
    
        return PredictionResponse(
            text=payload.url,
            prediction=y_pred,
            confidence_score= float(y_pred_proba),
            prediction_id=new_prediction.id,
            ssl_details=ssl_details_obj # Adicionado o detalhe SSL na resposta
        )

    @staticmethod
    def feedback(payload: FeedbackRequest, db: Session):
        prediction = db.query(Prediction).filter_by(id=payload.prediction_id).first()
    
        if not prediction:
            raise HTTPException(status_code=404, detail="Previsão não encontrada!")
    
        existing_feedback = db.query(Feedback).filter_by(prediction_id=payload.prediction_id).first()
        if existing_feedback:
            raise HTTPException(status_code=400, detail="Feedback para essa previsão já existe.")
    
        new_feedback = Feedback(
            prediction_id=payload.prediction_id,
            correct_label=payload.correct_label
        )
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)
        
        return FeedbackResponse(message="Feedback recebido com sucesso!")
        
ml_service = MlService()