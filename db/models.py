from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from db.database import Base

#Tabela que representa nosso modelo de IA com base em modelos preditivos.
# Ela armazena informações como nome, versão e data de criação do modelo.
class Model(Base):
    __tablename__ = 'model'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
<<<<<<< HEAD
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
=======
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
>>>>>>> ef1af0e88f079e4ea218900e468e80231e50c87d
    
    #Relação com as previsões feitas por nosso modelo.
    prediction_id = relationship("Prediction", back_populates="model")

#Esta tabela representa uma previsão feita pelo nosso modelo.
class Prediction(Base):
    __tablename__ = 'prediction'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
<<<<<<< HEAD
    input_text = Column(String, nullable=False)
    result = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
=======
    input_text = Column(String, nullable=False)
    result = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
>>>>>>> ef1af0e88f079e4ea218900e468e80231e50c87d
    
    model_id = Column(Integer, ForeignKey('model.id'))
    model = relationship("Model", back_populates="prediction_id")
