from pydantic import BaseModel

class PredictionCreate(BaseModel):
    url: str

class PredictionSchema(BaseModel):
    url: str
    prediction: str
    confidence: float
    probabilities: dict
    prediction_id: int