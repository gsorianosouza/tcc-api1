from services.ml_service import ml_service

class MlController:
    
    @staticmethod
    def predict(text: str):
        return ml_service.predict(text)
    
ml_controller = MlController()
    