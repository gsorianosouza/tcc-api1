from typing import List
from pydantic import BaseModel

class MetricsSchema(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    roc_auc: float
    confusion_matrix: List[List[int]]