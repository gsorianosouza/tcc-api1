from fastapi import BackgroundTasks
from services.model_service import model_service

class ModelController:
    
    @staticmethod
    def train_model(background_tasks: BackgroundTasks):
        background_tasks.add_task(model_service.train_model)
        return {"message": "Treinamento do modelo iniciado em background."}
    
model_controller = ModelController()