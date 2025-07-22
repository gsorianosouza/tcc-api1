from fastapi import APIRouter, Depends, HTTPException, Response
from db.models import Model
from db.models import Prediction
from schemas.model_schema import *
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.deps import get_db

router = APIRouter()

@router.get("/status", summary="Verifica o status da API")
def get_status():
    return {
        "status": "ok",
        "model_loaded": True,
        "model_version": "TF-IDF 1.0"
    }
      
@router.post("/add-model", summary="Adiciona um novo modelo", status_code=201, response_model=ModelResponse)
def add_model(model: ModelCreate, db: Session = Depends(get_db)):

    if not model.name or not model.version:
        raise HTTPException(status_code=400, detail="Nome e versão do modelo são obrigatórios!")

    existing_model = db.query(Model).filter(
        Model.name == model.name,
        Model.version == model.version
    ).first()
    
    if existing_model:
        raise HTTPException(status_code=400, detail="Não foi possível adicionar, o modelo já existe no banco de dados")

    existing_active_model = db.query(Model).filter(Model.is_active == True).first()
     
    new_model = Model( name=model.name, version=model.version, is_active= True if not existing_active_model else False )

    db.add(new_model)
    db.commit()
    db.refresh(new_model)

    return new_model

@router.delete("/delete-model/{model_id}", summary="Deleta um modelo existente")
def delete_model(model_id: int, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.id == model_id).first()
    
    if not model:
        raise HTTPException(status_code=404, detail="Modelo não encontrado")
    
    if model.is_active:
        raise HTTPException(status_code=400, detail="Não é possível deletar um modelo ativo. Por favor, ative outro modelo antes de deletar este.")
    
    db.delete(model)
    db.commit()

    return Response(status_code=204)

@router.get("/models", summary="Lista todos os modelos cadastrados", response_model=list[ModelResponse])
def list_models(db: Session = Depends(get_db)):
    models = db.query(Model).all()
    
    if not models:
        return []
    
    return models

@router.get("/predictions", summary="Lista o histórico de previsões")
def list_predictions(db: Session = Depends(get_db)):
    predictions = db.query(Prediction).all()

    if not predictions: 
        return []
    
    return predictions
    
@router.post("/models/{model_id}/activate", summary="Ativa ou alterna o modelo ativo")
def activate_model(model_id: int, db: Session = Depends(get_db)):
    model_to_activate = db.query(Model).filter(Model.id == model_id).first()
    
    if not model_to_activate:
        raise HTTPException(status_code=404, detail="Modelo não encontrado")
    
    if model_to_activate.is_active:
        raise HTTPException(status_code=400, detail="Este modelo já está ativo, por favor escolha outro")

    try:
        db.query(Model).filter(Model.is_active == True).update({"is_active": False})
        model_to_activate.is_active = True
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=500, detail="Erro ao atualizar o modelo ativo")
        
    return {
        "Message": f"Mudança de modelo realizada com sucesso! O modelo '{model_to_activate.name}' agora está ativo.",
        "Model": {
            "id": model_to_activate.id,
            "name": model_to_activate.name,
            "version": model_to_activate.version
        }
    }