from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path
from db.models import Feedback, Model
from schemas.feedback_schema import FeedbackResponse, FeedbackResponseFull, UpdateFeedbackRequest
from schemas.model_schema import ModelSchema
from sqlalchemy.orm import Session
from db.deps import get_db

router = APIRouter()

@router.get("/status", summary="Verifica o status da API")
def get_status():
    return {
        "status": "ok",
        "model_loaded": True,
        "model_version": "TF-IDF 1.0"
    }
    
@router.post("/add-model", summary="Adiciona um novo modelo")
def add_model(model: ModelSchema, db: Session = Depends(get_db)):

    if not model.name or not model.version:
        return { "Message": "Nome e versão do modelo são obrigatórios!"}
    
    existing_model = db.query(Model).filter(
        Model.name == model.name,
        Model.version == model.version
    ).first()
    
    if existing_model:
        return { "Message": "Não foi possível adicionar, o modelo já existe no banco de dados" }
    
    new_model = Model( name=model.name,version=model.version )

    db.add(new_model)
    db.commit()
    db.refresh(new_model)

    return {
        "Message": "Modelo adicionado com sucesso!",
        "Model": {
            "id": new_model.id,
            "name": new_model.name,
            "version": new_model.version,
            "created_at": new_model.created_at.isoformat()
        }
    }

@router.delete("/delete-model/{model_id}", summary="Deleta um modelo existente")
def delete_model(model_id: int, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.id == model_id).first()
    
    if not model:
        return { "Message": "Modelo não encontrado!" }
    
    db.delete(model)
    db.commit()
    
    return { "Message": "Modelo deletado com sucesso!" }

@router.get(
    "/feedback-list",
    response_model=List[FeedbackResponseFull],
    summary="Lista todos os feedbacks",
    description="Retorna todos os feedbacks armazenados no banco de dados."
)
def list_feedbacks(db: Session = Depends(get_db)):
    feedbacks = db.query(Feedback).all()
    return feedbacks

@router.put(
    "/feedback/{prediction_id}",
    response_model=FeedbackResponse,
    summary="Atualiza um feedback existente",
    description="Edita o campo 'correct_label' de um feedback com base no prediction_id."
)
def update_feedback(
    prediction_id: int,
    payload: UpdateFeedbackRequest,
    db: Session = Depends(get_db)
):
    feedback = db.query(Feedback).filter_by(prediction_id=prediction_id).first()

    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback não encontrado para essa previsão.")

    feedback.correct_label = payload.correct_label
    db.commit()
    db.refresh(feedback)

    return FeedbackResponse(message="Feedback atualizado com sucesso!")