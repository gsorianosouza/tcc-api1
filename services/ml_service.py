from fastapi import HTTPException
from core.config import settings
import joblib
from sqlalchemy.orm import Session
from db.models import Feedback, Model, Prediction
from views.schemas.feedback_schema import FeedbackRequest, FeedbackResponse
from views.schemas.prediction_schema import PredictionRequest, PredictionResponse

model = []

# joblib.load(settings.MODEL_PATH) OBS: preciso substituir aqui depois

class MlService:
    
    @staticmethod
    def predict(payload: PredictionRequest, db: Session):
        
        if not payload.text.strip():
            raise HTTPException(status_code=400, detail="O texto não pode ser vazio")
        
        prediction = model.predict([payload.text.strip()])
        
        model_record = db.query(Model).filter_by(name="TF-IDF", version="1.0").first()
        if not model_record:
            model_record = Model(name="TF-IDF", version="1.0")
            db.add(model_record)
            db.commit()
            db.refresh(model_record)
        
        new_prediction = Prediction(
            input_text=payload.text,
            result=str(prediction[0]),
            model_id=model_record.id
        )
        
        try:
            db.add(new_prediction)
            db.commit()
            db.refresh(new_prediction)
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao salvar a previsão: {e}")
    
        return PredictionResponse(text=payload.text, prediction=prediction[0], prediction_id=new_prediction.id)
    
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