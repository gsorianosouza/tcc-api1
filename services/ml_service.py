from core.config import settings
import joblib

model = joblib.load(settings.MODEL_PATH)

def predict(text: str) -> bool:
    result = model.predict([text.strip()])
    return bool(result[0])