from pydantic import BaseModel

class PredictionRequest(BaseModel):
    url: str

class PredictionResponse(BaseModel):
    text: str
    prediction: str
    confidence_score: float
    prediction_id: int
    