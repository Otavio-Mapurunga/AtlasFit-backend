#otavio eu vou dar commit no main.py mas como não sei se posso overwritar o teu, eu vou commitar e deixar tudo comentado
#blz valeu, tá la embaixo, depois do teu


from fastapi import FastAPI,HTTPException
from app.routes.ia_router import router
from fastapi.middleware.cors import CORSMiddleware
from app.routes.ia_router import router as ia_router
from app.routes.treino_router import router as treino_router

app= FastAPI()

app.include_router(ia_router)      
app.include_router(treino_router)

#config cors pro next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://v0-projeto-atlas-fit.vercel.app/"], 
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def red_road():
    return {"mensagem": "API funcionando"}


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

