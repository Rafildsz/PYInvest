from fastapi import FastAPI, HTTPException, status
from app.clients.clients import router as clients_router
from app.investments.investments import router as investments_router
from app.calculations.calculations import projecao, calcular_patrimonio
from app.yahoo_service.yahoo_service import obter_dados_mercado
from app.analytics.wallet import analisar_carteira
import requests

app = FastAPI(title="Investment Gateway Service")

app.include_router(clients_router)
app.include_router(investments_router)


DATA_SERVICE_URL = "http://127.0.0.1:8001/internal/clientes"
INVESTMENTS_SERVICE_URL = "http://127.0.0.1:8001/internal/investimentos"


@app.get("/api/v1/calculos/projecao/{cliente_id}")
def calcular_projecao(cliente_id: str):
    clientes = requests.get(DATA_SERVICE_URL).json()

    cliente = next((c for c in clientes if c["id"] == cliente_id), None)

    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
)

    return {
        "cliente": cliente["nome"],
        "perfil": cliente["perfil_investidor"],
        "projecao_anual": projecao(
            cliente["patrimonio_total"],
            cliente["perfil_investidor"]
        )
    }

@app.get("/api/v1/calculos/patrimonio/{cliente_id}")
def calcular_patrimonio_cliente(cliente_id: str):
    try:
        response = requests.get(
            f"{INVESTMENTS_SERVICE_URL}/cliente/{cliente_id}"
        )

        if response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado ou sem investimentos"
            )

        investimentos = response.json()

        if not investimentos:
            return {
                "cliente_id": cliente_id,
                "patrimonio_total": 0.0,
                "mensagem": "Cliente não possui investimentos"
            }

        patrimonio = calcular_patrimonio(investimentos)

        return {
            "cliente_id": cliente_id,
            "patrimonio_total": round(patrimonio, 2)
        }

    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço de investimentos indisponível"
        )


@app.get("/api/v1/analises/carteira/{cliente_id}")  
def analise_carteira(cliente_id: str):
    try:
        response = requests.get(
            f"{INVESTMENTS_SERVICE_URL}/cliente/{cliente_id}"
        )

        if response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado ou sem investimentos"
            )

        investimentos = response.json()

        if not investimentos:
            return {
                "cliente_id": cliente_id,
                "mensagem": "Cliente não possui investimentos cadastrados"
            }

        return analisar_carteira(cliente_id, investimentos)

    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Serviço de investimentos indisponível"
        )


@app.get("/api/v1/analises/mercado/{ticker}")
def analise_mercado(ticker: str):
    return obter_dados_mercado(ticker)



@app.get("/api/v1/analises/carteira/mercado/{cliente_id}")
def comparar_carteira_com_mercado(cliente_id: str):
    response = requests.get(
        f"{INVESTMENTS_SERVICE_URL}/cliente/{cliente_id}"
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado ou sem investimentos"
        )

    investimentos = response.json()

    if not investimentos:
        raise HTTPException(
            status_code=404,
            detail="Cliente não possui investimentos"
        )

    rentabilidade_carteira = round(
        sum(inv["rentabilidade"] for inv in investimentos) / len(investimentos),
        4
    )

    ticker_mercado = "AAPL"
    dados_mercado = obter_dados_mercado(ticker_mercado, periodo="1y")

    rentabilidade_mercado = dados_mercado["variacao_percentual"]

    if rentabilidade_carteira > rentabilidade_mercado:
        resultado = "CARTEIRA_SUPEROU_MERCADO"
    elif rentabilidade_carteira < rentabilidade_mercado:
        resultado = "MERCADO_SUPEROU_CARTEIRA"
    else:
        resultado = "EMPATE"

    return {
        "cliente_id": cliente_id,
        "carteira": {
            "rentabilidade_media": rentabilidade_carteira
        },
        "mercado": {
            "ticker": ticker_mercado,
            "rentabilidade_percentual": rentabilidade_mercado
        },
        "resultado": resultado
    }
