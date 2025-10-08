from pydantic_settings import BaseSettings
from pathlib import Path

class Settings (BaseSettings):
    PROJECT_NAME: str = "TCC-API"
    API_VERSION: str = "v1"
    
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    
    MODEL_PATH: Path = BASE_DIR / "model" / "rf_model.pkl"
    
    ENCODER_PATH: Path = BASE_DIR / "model" / "label_encoder.pkl"
    
    DATASET_PATH: Path = BASE_DIR / "model" / "dataset" / "malicious_phish.csv"
    
    METRICS_PATH: Path = BASE_DIR / "model" / "metrics.json"
    
    DATABASE_URL: str = "sqlite:///./test.db" 
    
    HOST: str = "0.0.0"
    PORT: int = 8000
    
    ALLOW_ORIGINS: list[str] = ["*"]
    class Config:
        env_file = ".env"
        
settings = Settings()