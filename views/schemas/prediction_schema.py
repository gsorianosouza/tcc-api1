from pydantic import BaseModel

class PredictionRequest(BaseModel):
    url: str

class PredictionResponse(BaseModel):
    url: str
    prediction: str
    confidence: float
    probabilities: dict
    prediction_id: int
    