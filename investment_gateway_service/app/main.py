from fastapi import FastAPI
from app.clients.clients import router as clients_router
from app.investments.investments import router as investments_router
from app.calculations.calculations import projecao, calcular_patrimonio
from app.yahoo_service.yahoo_service import obter_preco
import requests

app = FastAPI(title="Investment Gateway Service")

app.include_router(clients_router)
app.include_router(investments_router)

DATA_SERVICE_URL = "http://127.0.0.1:8001/internal/clientes"

@app.get("/api/v1/calculos/projecao/{cliente_id}")
def calcular_projecao(cliente_id: str):
    clientes = requests.get(DATA_SERVICE_URL).json()

    cliente = next((c for c in clientes if c["id"] == cliente_id), None)

    if not cliente:
        return {"erro": "Cliente não encontrado"}

    return {
        "cliente": cliente["nome"],
        "perfil": cliente["perfil_investidor"],
        "projecao_anual": projecao(
            cliente["patrimonio_total"],
            cliente["perfil_investidor"]
        )
    }

# terminar
@app.get("/api/v1/calculos/patrimonio/{cliente_id}")
def calcular_patrimonio_cliente(cliente_id: str):
    clientes = requests.get(DATA_SERVICE_URL).json()

    cliente = next((c for c in clientes if c["id"] == cliente_id), None)

    if not cliente:
        return {"erro": "Cliente não encontrado"}

    patrimonio_futuro = calcular_patrimonio(
        cliente["patrimonio_total"],
        cliente["aportes_mensais"]
    )

    return {
        "cliente": cliente["nome"],
        "patrimonio_atual": cliente["patrimonio_total"],
        "patrimonio_futuro": patrimonio_futuro
    }


@app.get("/api/v1/analises/mercado/{ticker}")
def analise_mercado(ticker: str):
    return obter_preco(ticker)

