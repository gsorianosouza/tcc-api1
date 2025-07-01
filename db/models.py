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
    name = Column(String, nullable=False)  #Nome do modelo.
    version = Column(String, nullable=False)  #Versão do modelo.
    created_at = Column(DateTime, default=datetime.now(timezone.utc))  #Data de criação.
=======
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
>>>>>>> ef1af0e88f079e4ea218900e468e80231e50c87d
    
    #Relação com as previsões feitas por nosso modelo.
    prediction_id = relationship("Prediction", back_populates="model")

#Esta tabela representa uma previsão feita pelo nosso modelo de IA.
class Prediction(Base):
    __tablename__ = 'prediction'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
<<<<<<< HEAD
    input_text = Column(String, nullable=False)  #Entrada usada na previsão.
    result = Column(String, nullable=False)  #Resultado da previsão.
    created_at = Column(DateTime, default=datetime.now(timezone.utc))  #Data da previsão.
=======
    input_text = Column(String, nullable=False)
    result = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
>>>>>>> ef1af0e88f079e4ea218900e468e80231e50c87d
    
    model_id = Column(Integer, ForeignKey('model.id'))  #ID do modelo que gerou a previsão.
    model = relationship("Model", back_populates="prediction_id")  #.Relação inversa com o nosso Model.
