from fastapi import APIRouter, WebSocket
from controllers.model_controller import model_controller

router = APIRouter()

@router.post("/train-model")
async def train_ml_model():
    return await model_controller.train_model()

@router.websocket("/ws/train-status")
async def websocket_train_status(websocket: WebSocket):
    await model_controller.websocket_endpoint(websocket)