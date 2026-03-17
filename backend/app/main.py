from fastapi import FastAPI

app= FastAPI()

@app.get("/")
def red_road():
    return {"mensagem: API funcionando"}