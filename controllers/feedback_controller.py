from services.feedback_service import feedback_service
from views.schemas.feedback_schema import UpdateFeedbackRequest
from sqlalchemy.orm import Session

class FeedbackController:
    @staticmethod
    def list_feedbacks(db: Session):
        return feedback_service.list_feedbacks(db)
    
feedback_controller = FeedbackController()