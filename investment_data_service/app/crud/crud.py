from sqlalchemy.orm import Session
from app.models.models import Cliente, Investimento
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

def criar_cliente(db: Session, cliente: Cliente):
    try:
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return cliente

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um cliente cadastrado com este CPF"
        )


def listar_clientes(db: Session):
    return db.query(Cliente).all()

def criar_investimento(db: Session, investimento):
    inv = Investimento(**investimento.dict())
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv

def listar_investimentos(db: Session):
    return db.query(Investimento).all()
