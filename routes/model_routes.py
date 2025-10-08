from fastapi import APIRouter
from controllers.model_controller import model_controller

router = APIRouter()

@router.post("/train-model")
def train_ml_model():
    return model_controller.train_model()