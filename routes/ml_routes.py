from fastapi import APIRouter

from services.ml_service import ml_service

router = APIRouter()

# @router.post("/predict")
# def predict(payload: PredictionRequest, db: Session = Depends(get_db)):
#     return ml_service.predict(payload)