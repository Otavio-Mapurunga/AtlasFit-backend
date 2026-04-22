#otavio eu vou dar commit no main.py mas como não sei se posso overwritar o teu, eu vou commitar e deixar tudo comentado
#blz valeu, tá la embaixo, depois do teu


from fastapi import FastAPI
from app.routes.ia_router import router

app= FastAPI()
app.include_router(router)

@app.get("/")
def red_road():
    return {"mensagem": "API funcionando"}

#from fastapi import FastAPI, HTTPException
#from fastapi.middleware.cors import CORSMiddleware
#from pydantic import BaseModel
#from projetoacademia import calcular_progressao, carga_sugerida, validar_treino

#app = FastAPI()

#####config cors pro next.js
#app.add_middleware(
#    CORSMiddleware,
#    allow_origins=["http://localhost:3000"],  # URL do seu front-end
#    allow_methods=["*"],
#    allow_headers=["*"],
#)

#class TreinoInput(BaseModel):
#    nivel: str
#    treinos_semana: int
#    reps: int
#    fadiga: bool = False

#@app.post("/api/treino/calcular")
#def calcular_treino(data: TreinoInput):
#    try:
#        nova = calcular_progressao(data.carga_atual, data.nivel)
#        sugerida = carga_sugerida(data.carga_atual, data.nivel, data.fadiga)
#        validacao = validar_treino(data.nivel, data.treinos_semana, data.reps)
#        return {
#            "nova_carga": nova,
#            "carga_sugerida": sugerida,
#            "validacao": validacao
#        }
#    except ValueError as e:
#        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
def root():
    return {"message": "API de Treino funcionando!"}
