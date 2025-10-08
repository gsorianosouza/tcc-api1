from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from db.database import Base

class Prediction(Base):
    __tablename__ = 'prediction'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    input_text = Column(String, nullable=False)
    result = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    feedbacks = relationship("Feedback", back_populates="prediction")

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prediction_id = Column(Integer, ForeignKey('prediction.id'))
    prediction = relationship("Prediction", back_populates="feedbacks")
    correct_label = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)