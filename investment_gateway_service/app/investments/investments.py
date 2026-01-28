from fastapi import APIRouter
import requests

router = APIRouter(tags=["Investimentos"])

DATA_SERVICE_URL = "http://127.0.0.1:8001/internal/investimentos"


@router.post("/api/v1/investimentos/")
def criar_investimento(investimento: dict):
    response = requests.post(DATA_SERVICE_URL, json=investimento)
    response.raise_for_status()
    return response.json()

@router.get("/api/v1/investimentos/")
def listar_investimentos():
    response = requests.get(DATA_SERVICE_URL)
    response.raise_for_status()
    return response.json()


@router.get("/api/v1/investimentos/cliente/{cliente_id}")
def listar_investimentos_por_cliente(cliente_id: str):
    investimentos = requests.get(DATA_SERVICE_URL).json()
    investimentos_cliente = [inv for inv in investimentos if inv["cliente_id"] == cliente_id]
    return investimentos_cliente


@router.delete("/api/v1/investimentos/{investimento_id}")
def deletar_investimento(investimento_id: str):
    response = requests.delete(f"{DATA_SERVICE_URL}/{investimento_id}")
    response.raise_for_status()
    return response.json()
