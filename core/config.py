from pydantic_settings import BaseSettings
from pathlib import Path

class Settings (BaseSettings):
    # Configurações gerais da API, como nome e versão.
    PROJECT_NAME: str = "TCC-API"
    API_VERSION: str = "v1"
    
    # Caminho base do projeto.
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    
    # Caminho do modelo utilizado pela API.
    MODEL_PATH: Path = BASE_DIR / "model" / "model.pkl"
    
    #Configurações do banco de dados.
    DATABASE_URL: str
    
    # Configurações do servidor.
    HOST: str = "0.0.0"
    PORT: int = 8000
    
    # Configurações CORS (Cross-Origin Resource Sharing), utilizadas para permitir requisições de diferentes origens.
    ALLOW_ORIGINS: list[str] = ["*"]
    # Configurações de segurança, como chaves secretas.
    class Config:
        env_file = ".env"
        
settings = Settings()