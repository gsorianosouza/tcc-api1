from fastapi import HTTPException
from ml.models.feedback import Feedback
from sqlalchemy.orm import Session
from ml.models.prediction import Prediction
from ml.schemas.feedback import FeedbackRequest, FeedbackResponse

def get_feedbacks(db: Session):
    return db.query(Feedback).all()

def update_feedback(prediction_id: int, payload: FeedbackRequest, db: Session) -> FeedbackResponse:
    prediction = db.query(Prediction).filter_by(id=prediction_id).first()
    
    if not prediction:
        raise HTTPException(status_code=404, detail="Previsão não encontrada!")

    existing_feedback = db.query(Feedback).filter_by(prediction_id=prediction_id).first()
    
    if existing_feedback:
        existing_feedback.correct_label = payload.correct_label
        message = "Feedback atualizado com sucesso!"
    else:
        new_feedback = Feedback(
            prediction_id=prediction_id,
            correct_label=payload.correct_label
        )
        db.add(new_feedback)
        message = "Feedback enviado com sucesso!"

    prediction.result = payload.correct_label

    db.commit()
    db.refresh(prediction)

    return FeedbackResponse(message=message)
