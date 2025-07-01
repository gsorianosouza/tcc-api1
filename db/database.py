from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv, find_dotenv
import os

#Carrega variáveis de ambiente do arquivo .env.
load_dotenv(override=True)

#Obtém a URL do banco de dados a partir das variáveis de ambiente.
DATABASE_URL = os.getenv("DATABASE_URL")

#Cria a conexão com o banco de dados.
engine = create_engine(DATABASE_URL) # type: ignore

#Cria uma sessão de banco de dados configurada.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base para definição dos modelos ORM.
Base = declarative_base()
