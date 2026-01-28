def projecao(patrimonio: float, perfil: str):
    if perfil == "CONSERVADOR":
        return patrimonio * 0.08
    if perfil == "MODERADO":
        return patrimonio * 0.12
    if perfil == "ARROJADO":
        return patrimonio * 0.18
    else:
        return "Perfil de investidor inválido"
