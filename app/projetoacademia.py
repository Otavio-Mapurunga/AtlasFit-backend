def calcular_progressao(carga_atual, nivel):
taxas = {
        "iniciante": 0.05,
"intermediario": 0.025,
        "avancado": 0.01
    }
    if nivel not in taxas:
        raise ValueError("Nível inválido")
    return round(carga_atual * (1 + taxas[nivel]), 2)
def definir_regras(nivel):
