from fastapi import FastAPI
from app.routes.ia_router import router

app= FastAPI()
app.include_router(router)

@app.get("/")
def red_road():
    return {"mensagem": "API funcionando"}