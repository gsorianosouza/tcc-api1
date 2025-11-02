from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from core.config_loader import settings

from auth.routes.auth_router import auth_router
from user.routes.user_router import user_router
from ml.routes.ml_router import ml_router

app = FastAPI(title=settings.PROJECT_NAME, version=settings.API_VERSION)

@app.get("/",tags=["Home"], summary="Rota inicial da API")
def read_root():
    return "Seja Bem-vindo à TrustLink API!"

@app.get("/status",tags=["Home"], summary="Checagem para ver se a API está online")
def status_check():
    return {"Status": "OK"}

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
app.include_router(ml_router)
app.include_router(user_router)
app.include_router(auth_router)
