from pydantic import BaseModel

class PredictionRequest(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    text: str
    prediction: str
    prediction_id: int
    