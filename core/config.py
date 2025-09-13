from pydantic_settings import BaseSettings
from pathlib import Path

class Settings (BaseSettings):
    PROJECT_NAME: str = "TCC-API"
    API_VERSION: str = "v1"
    
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    
    MODEL_PATH: Path = BASE_DIR / "model" / "XGBoostClassifier.pickle.dat"
        
    DATA_PATH: Path = BASE_DIR / "model" / "dataset" / "Phishing_Legitimate_full.csv"
    
    DATABASE_URL: str = "sqlite:///./test.db"
    
    HOST: str = "0.0.0"
    PORT: int = 8000
    
    ALLOW_ORIGINS: list[str] = ["*"]
    class Config:
        env_file = ".env"
        
settings = Settings()