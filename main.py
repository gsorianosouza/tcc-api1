from fastapi import FastAPI
from routes import system_routes, ml_routes

app = FastAPI();

@app.get("/",tags=["Home"], summary="Rota inicial da API")
def read_root():
    return "Seja Bem-vindo à API!"

app.include_router(system_routes.router, tags= ["Sistema"])
app.include_router(ml_routes.router, prefix="/model", tags=["Machine Learning"])