from fastapi import FastAPI

app = FastAPI(
    title="DevShowcase API",
    description="API para gerenciamento de perfis, projetos, tecnologias e feedbacks.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "DevShowcase API está funcionando!"
    }