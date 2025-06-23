from core.config import settings
import joblib

model = joblib.load(settings.MODEL_PATH)

def predict(text: str):
    result = model.predict([text])
    return result[0]