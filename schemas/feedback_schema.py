from pydantic import BaseModel

class FeedbackRequest(BaseModel):
    prediction_id: int
    correct_label: bool

class FeedbackResponse(BaseModel):
    message: str