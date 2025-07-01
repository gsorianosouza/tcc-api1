from fastapi import APIRouter

router = APIRouter()

#Rota para verificar se a API está funcionando e qual versão do modelo está carregada.
@router.get("/status", summary="Verifica o status da API")
def get_status():
    return {
        "status": "ok",
        "model_loaded": True,
        "model_version": "TF-IDF 1.0"
    }
