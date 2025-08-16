from core.config import settings
import joblib

model = joblib.load(settings.MODEL_PATH)

class MlService:
    
    @staticmethod
    def predict(text: str) -> bool:
        result = model.predict([text.strip()])
        return bool(result[0])
    
ml_service = MlService()