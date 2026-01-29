def projecao(patrimonio: float, perfil: str):
    if perfil == "CONSERVADOR":
        return patrimonio * 0.08
    if perfil == "MODERADO":
        return patrimonio * 0.12
    if perfil == "ARROJADO":
        return patrimonio * 0.18
    return 0.0

# terminar
def calcular_patrimonio(patrimonio: float, aportes_mensais: float = 0.0):
    taxa_juros_mensal = 0.01  # Exemplo de taxa fixa mensal de 1%
    patrimonio_futuro = patrimonio

    for _ in range(12):  # Calcula para 12 meses
        patrimonio_futuro = (patrimonio_futuro + aportes_mensais) * (1 + taxa_juros_mensal)

    return patrimonio_futuro
