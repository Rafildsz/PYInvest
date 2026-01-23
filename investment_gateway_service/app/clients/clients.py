from fastapi import APIRouter
import requests

router = APIRouter(prefix="/api/v1/clientes", tags=["Clientes"])

DATA_SERVICE_URL = "http://127.0.0.1:8001/internal/clientes"


@router.get("/")
def listar_clientes():
    response = requests.get(DATA_SERVICE_URL)
    response.raise_for_status()
    return response.json()


@router.get("/{cliente_id}")
def buscar_cliente(cliente_id: str):
    clientes = requests.get(DATA_SERVICE_URL).json()
    cliente = next((c for c in clientes if c["id"] == cliente_id), None)

    if not cliente:
        return {"erro": "Cliente não encontrado"}

    return cliente


@router.post("/")
def criar_cliente(cliente: dict):
    response = requests.post(DATA_SERVICE_URL, json=cliente)
    response.raise_for_status()
    return response.json()


@router.delete("/{cliente_id}")
def deletar_cliente(cliente_id: str):
    return {
        "mensagem": "DELETE básico não implementado no Data Service (opcional)",
        "cliente_id": cliente_id
    }
