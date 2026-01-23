def projecao(patrimonio: float, perfil: str):
    if perfil == "CONSERVADOR":
        return patrimonio * 0.08
    if perfil == "MODERADO":
        return patrimonio * 0.12
    return patrimonio * 0.18
