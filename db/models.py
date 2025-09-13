from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from db.database import Base

#Tabela que representa nosso modelo de IA com base em modelos preditivos.
# Ela armazena informações como nome, versão e data de criação do modelo.
class Model(Base):
    __tablename__ = 'model'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=False) 

    # Relação com as previsões feitas por nosso modelo.
    prediction_id = relationship("Prediction", back_populates="model")

#Esta tabela representa uma previsão feita pelo nosso modelo.
class Prediction(Base):
    __tablename__ = 'prediction'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    input_text = Column(String, nullable=False)
    result = Column(String, nullable=False)
    confidence_score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    model_id = Column(Integer, ForeignKey('model.id'))
    model = relationship("Model", back_populates="prediction_id")

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prediction_id = Column(Integer, nullable=False)
    correct_label = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.now)