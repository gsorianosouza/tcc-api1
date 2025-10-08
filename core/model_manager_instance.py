from core.config import settings
from core.model_manager import ModelManager


model_manager = ModelManager(
    model_path=settings.MODEL_PATH,
    encoder_path=settings.ENCODER_PATH,
    metrics_path=settings.METRICS_PATH
)