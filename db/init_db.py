from db.database import engine
from db import models

def init_db():
    #Função para inicializar o nosso banco de dados. Ela cria todas as tabelas definidas em models.py, caso ainda não existam.
    print("Inicializando o banco de dados...")
    
    models.Base.metadata.create_all(bind=engine)
    
    print("Tabelas criadas com sucesso!")
#Executa a função ao rodar o script diretamente.
if __name__ == "__main__":
    init_db()