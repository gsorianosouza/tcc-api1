from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from db.database import Base

class Model(Base):
    __tablename__ = 'model'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    
    prediction_id = relationship("Prediction", back_populates="model")
    
class Prediction(Base):
    __tablename__ = 'prediction'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    input_text = Column(String, nullable=False)
    result = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    
    model_id = Column(Integer, ForeignKey('model.id'))
    model = relationship("Model", back_populates="prediction_id")