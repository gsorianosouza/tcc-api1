from fastapi import APIRouter, HTTPException, Depends
from schemas.feedback_schema import *
from schemas.prediction_schema import *
from services import ml_service
from db.models import Feedback, Model, Prediction
from db.deps import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/predict", response_model= PredictionResponse, summary="Faz uma previsão com o modelo", description="Recebe um texto e retorna se é verdadeiro ou falso.")
def predict(payload: PredictionRequest, db: Session = Depends(get_db)):
    prediction = ml_service.predict(payload.text)
    
    # Verifica se o modelo já existe no banco de dados, caso contrário, cria um novo registro
    model_record = db.query(Model).filter_by(id=1).first()
    if not model_record:
        model_record = Model(name="TF-IDF", version="1.0")
        db.add(model_record)
        db.commit()
        db.refresh(model_record)
        
    # Cria uma nova previsão no banco de dados
    new_prediction = Prediction(
        input_text=payload.text,
        result=str(prediction),
        model_id=model_record.id
    )
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)
    
    return PredictionResponse(text=payload.text, prediction=prediction, prediction_id=new_prediction.id)

@router.post("/feedback", 
             response_model=FeedbackResponse, 
             summary="Envia feedback sobre uma previsão", 
             description="Recebe o ID da previsão e se a previsão estava correta ou não.")
def send_feedback(payload: FeedbackRequest, db: Session = Depends(get_db)):
    # Verifica se a previsão existe no banco de dados
    prediction = db.query(Prediction).filter_by(id=payload.prediction_id).first()
    
    if not prediction:
        raise HTTPException(status_code=404, detail="Previsão não encontrada!")
    
    existing_feedback = db.query(Feedback).filter_by(prediction_id=payload.prediction_id).first()
    if existing_feedback:
        raise HTTPException(status_code=400, detail="Feedback para essa previsão já existe.")
    
    # Cria um novo feedback no banco de dados
    new_feedback = Feedback(
        prediction_id=payload.prediction_id,
        correct_label=payload.correct_label
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    
    return FeedbackResponse(message="Feedback recebido com sucesso!")