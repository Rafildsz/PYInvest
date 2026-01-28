from fastapi import APIRouter, HTTPException
import requests

router = APIRouter(tags=["Clientes"])

DATA_SERVICE_URL = "http://127.0.0.1:8001/internal/clientes"


@router.post("/api/v1/clientes/")
def criar_cliente(cliente: dict):
    response = requests.post(DATA_SERVICE_URL, json=cliente)
    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json().get("detail")
    )
    return response.json()


@router.get("/api/v1/clientes/")
def listar_clientes():
    response = requests.get(DATA_SERVICE_URL)
    response.raise_for_status()
    return response.json()


@router.get("/api/v1/clientes/{cliente_id}")
def listar_cliente_por_id(cliente_id: str):
    response = requests.get(f"{DATA_SERVICE_URL}/{cliente_id}")
    if response.status_code == 404:
        return {"erro": "Cliente não encontrado"}
    response.raise_for_status()
    return response.json()


@router.put("/api/v1/clientes/{cliente_id}")
def atualizar_cliente(cliente_id: str, cliente_atualizado: dict):
    response = requests.put(f"{DATA_SERVICE_URL}/{cliente_id}", json=cliente_atualizado)
    response.raise_for_status()
    return response.json()


@router.delete("/api/v1/clientes/{cliente_id}")
def deletar_cliente(cliente_id: str):
    response = requests.delete(f"{DATA_SERVICE_URL}/{cliente_id}")
    if response.status_code >= 400:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json().get("detail")
    )
    return response.json()
