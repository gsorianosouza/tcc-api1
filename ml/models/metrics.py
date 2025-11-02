from sqlalchemy import Column, Float, JSON, Integer
from core.database import Base

class Metrics(Base):
    __tablename__ = 'metrics'
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    accuracy = Column(Float, index=True, nullable=False)
    precision = Column(Float, index=True, nullable=False)
    recall = Column(Float, index=True, nullable=False)
    f1_score = Column(Float ,index=True, nullable=False)
    roc_auc = Column(Float, index=True, nullable=False)
    confusion_matrix = Column(JSON, nullable=False)