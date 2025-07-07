from fastapi import APIRouter, Depends
from db.models import Model, Sources
from schemas.model_schema import ModelSchema
from schemas.source_schema import SourceSchema
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

@router.get("/model/list", summary="Lista todos os modelos")
def list_models(db: Session = Depends(get_db)):
    models = db.query(Model).all()
    return {
        "models": [
            {
                "id": model.id,
                "name": model.name,
                "version": model.version,
                "created_at": model.created_at.isoformat()
            } for model in models
        ]
    }

@router.post("/model/add", summary="Adiciona um novo modelo")
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

@router.get("/source/list", summary="Lista a quantidade de fontes")
def list_source(db: Session = Depends(get_db)):
    sources_count = db.query(Sources).count()
    
    if sources_count == 0:
        return {"message": "Nenhuma fonte encontrada."}
    else:
        return {"quantidade_de_fontes": sources_count}
    
@router.post("/source/add", summary="Adiciona uma nova fonte")
def add_source(source: SourceSchema, db: Session = Depends(get_db)):

    if not source.link or not source.description:
        return { "Message": "Nome e versão do modelo são obrigatórios!"}
    
    existing_source = db.query(Sources).filter(
    Sources.link == source.link
    ).first()

    
    if existing_source:
        return { "Message": "Não foi possível adicionar, essa fonte já existe no banco de dados" }
    
    new_source = Sources( link=source.link, description=source.description)

    db.add(new_source)
    db.commit()
    db.refresh(new_source)

    return {
        "Message": "Fonte adicionada com sucesso!",
        "Model": {
            "id": new_source.id,
            "link": new_source.link,
            "description": new_source.description,
            "created_at": new_source.created_at.isoformat()
        }
    }