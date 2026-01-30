def projecao(patrimonio: float, perfil: str):
    if perfil == "CONSERVADOR":
        return patrimonio * 0.08
    if perfil == "MODERADO":
        return patrimonio * 0.12
    if perfil == "ARROJADO":
        return patrimonio * 0.18
    return 0.0


def calcular_patrimonio(investimentos: list) -> float:
    total = 0.0

    for inv in investimentos:
        if inv.get("ativo"):
            valor = inv["valor_investido"]
            rendimento = valor * inv["rentabilidade"]
            total += valor + rendimento

    return total




