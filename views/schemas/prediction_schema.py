from typing import Optional
from pydantic import BaseModel

class SSLDetails(BaseModel):
    issued_to: Optional[str] = None
    issued_by: Optional[str] = None
    valid_until: Optional[str] = None

class PredictionRequest(BaseModel):
    url: str

class PredictionResponse(BaseModel):
    text: str
    prediction: str
    confidence_score: float
    prediction_id: int
    ssl_details: Optional[SSLDetails] = None
    