from app.projetoacademia import calcular_progressao, carga_sugerida, validar_treino
#viado n é possível
def calcular_progressao(carga_atual: float, nivel: str) -> float:
    taxas = {
        "iniciante": 0.05,
        "intermediario": 0.025,
        "avancado": 0.01
    }
    if nivel not in taxas:
        raise ValueError("Nível inválido")
    return round(carga_atual * (1 + taxas[nivel]), 2)


def carga_sugerida(carga_atual: float, nivel: str, fadiga: bool = False) -> float:
    nova = calcular_progressao(carga_atual, nivel)
    if fadiga:
        nova *= 0.9
    return round(nova, 2)


def validar_treino(nivel: str, treinos_semana: int, reps: int) -> dict:
    regras = {
        "iniciante":     {"max_treinos_semana": 3, "range_reps": (10, 15)},
        "intermediario": {"max_treinos_semana": 5, "range_reps": (8, 12)},
        "avancado":      {"max_treinos_semana": 6, "range_reps": (6, 10)}
    }
    r = regras.get(nivel)
    if not r:
        raise ValueError("Nível inválido")
    erros = []
    if treinos_semana > r["max_treinos_semana"]:
        erros.append("Treinos semanais acima do recomendado")
    if not (r["range_reps"][0] <= reps <= r["range_reps"][1]):
        erros.append("Repetições fora do ideal")
    return {"valido": len(erros) == 0, "erros": erros}