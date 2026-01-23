from fastapi import FastAPI
from app.clients.clients import router as clients_router
from app.investments.investments import router as investments_router
from app.calculations.calculations import projecao
from app.yahoo_service.yahoo_service import obter_preco
import requests

app = FastAPI(title="Investment Gateway Service")

app.include_router(clients_router)
app.include_router(investments_router)


@app.get("/api/v1/calculos/projecao/{cliente_id}")
def calcular_projecao(cliente_id: str):
    clientes = requests.get(
        "http://127.0.0.1:8001/internal/clientes"
    ).json()

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


@app.get("/api/v1/analises/mercado/{ticker}")
def analise_mercado(ticker: str):
    return obter_preco(ticker)

