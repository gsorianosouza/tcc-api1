from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from db.database import Base

#Tabela que representa nosso modelo de IA com base em modelos preditivos.
# Ela armazena informações como nome, versão e data de criação do modelo.
class Model(Base):
    __tablename__ = 'model'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)  #Nome do modelo.
    version = Column(String, nullable=False)  #Versão do modelo.
    created_at = Column(DateTime, default=datetime.now(timezone.utc))  #Data de criação.
    
    #Relação com as previsões feitas por nosso modelo.
    prediction_id = relationship("Prediction", back_populates="model")

#Esta tabela representa uma previsão feita pelo nosso modelo de IA.
class Prediction(Base):
    __tablename__ = 'prediction'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    input_text = Column(String, nullable=False)  #Entrada usada na previsão.
    result = Column(String, nullable=False)  #Resultado da previsão.
    created_at = Column(DateTime, default=datetime.now(timezone.utc))  #Data da previsão.
    
    model_id = Column(Integer, ForeignKey('model.id'))  #ID do modelo que gerou a previsão.
    model = relationship("Model", back_populates="prediction_id")  #.Relação inversa com o nosso Model.
