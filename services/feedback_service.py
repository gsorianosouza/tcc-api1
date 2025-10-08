from fastapi import HTTPException
from db.models import Feedback
from views.schemas.feedback_schema import UpdateFeedbackRequest, FeedbackResponse
from sqlalchemy.orm import Session

class FeedbackController: 

    @staticmethod
    def list_feedbacks(db: Session):
            return db.query(Feedback).all()

    
feedback_service = FeedbackController()   