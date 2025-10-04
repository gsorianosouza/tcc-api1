from fastapi import HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.models import Model
from views.schemas.model_schema import ModelCreate

class ModelService:
    
    @staticmethod
    def delete_model(model_id: int, db: Session):
        model = db.query(Model).filter(Model.id == model_id).first()
        
        if not model:
            raise HTTPException(status_code=404, detail="Modelo não encontrado")
        
        if model.is_active:
            raise HTTPException(status_code=400, detail="Não é possível deletar um modelo ativo.")

        db.delete(model)
        db.commit()

        return Response(status_code=204)
    
    @staticmethod
    def list_models(db: Session):
        return db.query(Model).all()

    @staticmethod
    def activate_model(model_id: int, db: Session):
        model_to_activate = db.query(Model).filter(Model.id == model_id).first()
        
        if not model_to_activate:
            raise HTTPException(status_code=404, detail="Modelo não encontrado")
        
        if model_to_activate.is_active:
            raise HTTPException(status_code=400, detail="Este modelo já está ativo")

        try:
            db.query(Model).filter(Model.is_active == True).update({"is_active": False})
            model_to_activate.is_active = True
            db.commit()
        except IntegrityError:
            raise HTTPException(status_code=500, detail="Erro ao atualizar o modelo ativo")
            
        return {
            "Message": f"Modelo '{model_to_activate.name}' agora está ativo.",
            "Model": {
                "id": model_to_activate.id,
                "name": model_to_activate.name,
                "version": model_to_activate.version
            }
        }

model_service = ModelService()