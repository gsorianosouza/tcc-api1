from fastapi import FastAPI
from routes import system_routes, ml_routes
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.API_VERSION);

@app.get("/",tags=["Home"], summary="Rota inicial da API")
def read_root():
    return "Seja Bem-vindo à API!"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.ALLOW_ORIGINS] if isinstance(settings.ALLOW_ORIGINS, str) else settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(system_routes.router, tags= ["Sistema"])
app.include_router(ml_routes.router, prefix="/model", tags=["Machine Learning"])