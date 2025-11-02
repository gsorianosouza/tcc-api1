from sqlalchemy.orm import Session

from ml.models.metrics import Metrics

def get_metrics(db: Session):
    return db.query(Metrics).all()