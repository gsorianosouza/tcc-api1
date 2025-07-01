from db.database import SessionLocal

#Fornece uma sessão de banco de dados para uso temporário
def get_db():
    db = SessionLocal()
    try:
        yield db  #Retorna a sessão para ser usada em dependências.
    finally:
        db.close()  #Garante que a sessão será fechada após o uso.
