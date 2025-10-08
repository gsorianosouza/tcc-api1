from fastapi import APIRouter, Depends
from controllers.ml_controller import ml_controller
from db.deps import get_db
from services.prediction_service import prediction_service
from views.schemas.prediction_schema import PredictionRequest
from views.schemas.feedback_schema import FeedbackRequest, FeedbackResponse
from sqlalchemy.orm import Session
from services.ml_service import MlService

router = APIRouter()

@router.post("/predict")
def make_prediction(payload: PredictionRequest, db: Session = Depends(get_db)):
    return ml_controller.predict(payload, db)

@router.put("/feedback/{prediction_id}", response_model=FeedbackResponse)
def make_feedback(prediction_id: int, payload: FeedbackRequest, db: Session = Depends(get_db)):
    return ml_controller.feedback(prediction_id, payload, db)

@router.get("/metrics")
def get_model_metrics():
    return {"model_metrics": MlService.get_metrics()}