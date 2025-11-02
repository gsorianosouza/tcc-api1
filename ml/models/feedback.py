from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prediction_id = Column(Integer, ForeignKey('prediction.id'))
    prediction = relationship("Prediction", back_populates="feedbacks")
    correct_label = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))