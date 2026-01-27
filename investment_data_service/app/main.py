from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database.database import Base, engine, SessionLocal
from app.schemas.schemas import ClienteCreate, ClienteUpdate ,InvestimentoCreate, InvestimentoUpdate
from app.crud.crud import *

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Clientes

@app.post("/internal/clientes")
def criar(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return criar_cliente(db, cliente)

@app.get("/internal/clientes")
def listar(db: Session = Depends(get_db)):
    return listar_clientes(db)

@app.get("/internal/clientes/{cliente_id}")
def buscar(cliente_id: str, db: Session = Depends(get_db)):
    cliente = listar_cliente_por_id(db, cliente_id)
    if not cliente:
        return {"erro": "Cliente não encontrado"}
    return cliente

@app.put("/internal/clientes/{cliente_id}")
def atualizar(cliente_id: str, cliente_update: ClienteUpdate, db: Session = Depends(get_db)):
    cliente = atualizar_cliente(db, cliente_id, cliente_update.dict())
    return cliente

@app.delete("/internal/clientes/{cliente_id}")
def deletar(cliente_id: str, db: Session = Depends(get_db)):
    return deletar_cliente(db, cliente_id)

# Investimentos

@app.post("/internal/investimentos")
def criar_inv(inv: InvestimentoCreate, db: Session = Depends(get_db)):
    return criar_investimento(db, inv)

@app.get("/internal/investimentos")
def listar_inv(db: Session = Depends(get_db)):
    return listar_investimentos(db)

@app.get("/internal/investimentos/{investimento_id}")
def buscar_inv(investimento_id: str, db: Session = Depends(get_db)):
    investimento = listar_investimento_por_id(db, investimento_id)
    if not investimento:
        return {"erro": "Investimento não encontrado"}
    return investimento

@app.put("/internal/investimentos/{investimento_id}")
def atualizar_inv(investimento_id: str, inv_update: InvestimentoUpdate, db: Session = Depends(get_db)):
    investimento = atualizar_investimento(db, investimento_id, inv_update.dict())
    return investimento

@app.delete("/internal/investimentos/{investimento_id}")
def deletar_inv(investimento_id: str, db: Session = Depends(get_db)):
    return deletar_investimento(db, investimento_id)
