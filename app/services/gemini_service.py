from app.config import client
def gerar_treino(prompt :str):
    response=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "max_output_tokens":8000,
            "temperature":0.7 }      
    )
    return response.text