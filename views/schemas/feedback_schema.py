from pydantic import BaseModel

class FeedbackRequest(BaseModel):
    correct_label: str

class UpdateFeedbackRequest(BaseModel):
    correct_label: str

class FeedbackResponse(BaseModel):
    message: str

class FeedbackResponseFull(BaseModel):
    id: int
    prediction_id: int
    correct_label: str

    model_config = {
        "from_attributes": True
    }