from fastapi import FastAPI

from .database import Base, engine
from . import models
from .routes import profiles, technologies, projects


# Cria as tabelas do banco de dados
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="DevShowcase API",
    description="API para gerenciamento de perfis, projetos, tecnologias e feedbacks.",
    version="1.0.0"
)


# Rotas da API
app.include_router(profiles.router)
app.include_router(technologies.router)
app.include_router(projects.router)


@app.get("/")
def root():
    return {
        "message": "DevShowcase API está funcionando!"
    }