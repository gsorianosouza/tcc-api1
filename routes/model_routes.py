from fastapi import APIRouter, BackgroundTasks
from controllers.model_controller import model_controller

router = APIRouter()

@router.post("/train-model")
def train_ml_model(background_tasks: BackgroundTasks):
    return model_controller.train_model(background_tasks)