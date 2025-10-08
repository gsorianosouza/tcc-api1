from pydantic_settings import BaseSettings
from pathlib import Path
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "TCC-API"
    API_VERSION: str = "v1"
    
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    
    MODEL_PATH: Path = Path(os.getenv("MODEL_PATH", BASE_DIR / "model" / "rf_model.pkl"))
    ENCODER_PATH: Path = Path(os.getenv("ENCODER_PATH", BASE_DIR / "model" / "label_encoder.pkl"))
    DATASET_PATH: Path = Path(os.getenv("DATASET_PATH", BASE_DIR / "model" / "dataset" / "malicious_phish.csv"))
    METRICS_PATH: Path = Path(os.getenv("METRICS_PATH", BASE_DIR / "model" / "metrics.json"))
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    
    ALLOW_ORIGINS: list[str] = os.getenv("ALLOW_ORIGINS", '["*"]').replace("'", '"')
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()