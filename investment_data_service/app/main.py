from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database.database import Base, engine, SessionLocal
from app.schemas.schemas import ClienteCreate, InvestimentoCreate
from app.crud.crud import *

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/internal/clientes")
def criar(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return criar_cliente(db, cliente)

@app.get("/internal/clientes")
def listar(db: Session = Depends(get_db)):
    return listar_clientes(db)

@app.post("/internal/investimentos")
def criar_inv(inv: InvestimentoCreate, db: Session = Depends(get_db)):
    return criar_investimento(db, inv)

@app.get("/internal/investimentos")
def listar_inv(db: Session = Depends(get_db)):
    return listar_investimentos(db)
