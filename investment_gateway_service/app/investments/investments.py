from fastapi import APIRouter
import requests

router = APIRouter(prefix="/api/v1/investimentos", tags=["Investimentos"])

DATA_SERVICE_URL = "http://127.0.0.1:8001/internal/investimentos"


@router.get("/")
def listar_investimentos():
    response = requests.get(DATA_SERVICE_URL)
    response.raise_for_status()
    return response.json()


@router.get("/cliente/{cliente_id}")
def listar_por_cliente(cliente_id: str):
    investimentos = requests.get(DATA_SERVICE_URL).json()
    return [i for i in investimentos if i["cliente_id"] == cliente_id]


@router.post("/")
def criar_investimento(investimento: dict):
    response = requests.post(DATA_SERVICE_URL, json=investimento)
    response.raise_for_status()
    return response.json()


@router.delete("/{investimento_id}")
def deletar_investimento(investimento_id: str):
    return {
        "mensagem": "DELETE básico não implementado no Data Service (opcional)",
        "investimento_id": investimento_id
    }
