from db.database import engine
from db import models

def init_db():
    print("Inicializando o banco de dados...")
    
    models.Base.metadata.create_all(bind=engine)
    
    print("Tabelas criadas com sucesso!")
if __name__ == "__main__":
    init_db()