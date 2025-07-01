from fastapi import APIRouter, Depends
from schemas.model_schema import ModelSchema
from sqlalchemy.orm import Session
from db.deps import get_db
from db.models import Model

router = APIRouter()

@router.get("/status", summary="Verifica o status da API")
def get_status():
    return {
        "status": "ok",
        "model_loaded": True,
        "model_version": "TF-IDF 1.0"
    }
<<<<<<< HEAD
=======
    
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
>>>>>>> ef1af0e88f079e4ea218900e468e80231e50c87d
