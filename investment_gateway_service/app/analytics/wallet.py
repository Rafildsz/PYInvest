import pandas as pd

def analisar_carteira(cliente_id: str, investimentos: list):
    df = pd.DataFrame(investimentos)

    if "ativo" in df.columns:
        df = df[df["ativo"] == True]

    if df.empty:
        return {
            "cliente_id": cliente_id,
            "mensagem": "Nenhum investimento ativo encontrado"
        }

    total_investido = df["valor_investido"].sum()

    retorno_total = (
        df["valor_investido"] * df["rentabilidade"]
    ).sum()

    rentabilidade_media = retorno_total / total_investido

    distribuicao_por_tipo = (
        df.groupby("tipo_investimento")["valor_investido"]
        .sum()
        .to_dict()
    )

    return {
        "cliente_id": cliente_id,
        "total_investido": round(total_investido, 2),
        "retorno_total": round(retorno_total, 2),
        "rentabilidade_media": round(rentabilidade_media, 4),
        "distribuicao_por_tipo": distribuicao_por_tipo
    }
