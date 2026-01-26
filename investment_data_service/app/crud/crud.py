from sqlalchemy.orm import Session
from app.schemas.schemas import ClienteCreate, InvestimentoCreate
from app.models.models import Cliente, Investimento
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status


def criar_cliente(db: Session, cliente: ClienteCreate):
    cliente_db = Cliente(
        nome=cliente.nome,
        cpf=cliente.cpf,
        email=cliente.email,
        perfil_investidor=cliente.perfil_investidor,
        patrimonio_total=cliente.patrimonio_total
    )

    try:
        db.add(cliente_db)
        db.commit()
        db.refresh(cliente_db)
        return cliente_db

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um cliente cadastrado com este CPF"
        )




def listar_clientes(db: Session):
    return db.query(Cliente).all()

def listar_cliente_por_id(db: Session, cliente_id: str):
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()

def atualizar_cliente(db: Session, cliente_id: str, dados_atualizados: dict):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    for key, value in dados_atualizados.items():
        setattr(cliente, key, value)
    db.commit()
    db.refresh(cliente)
    return cliente

def deletar_cliente(db: Session, cliente_id: str):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )
    db.delete(cliente)
    db.commit()
    return {"mensagem": "Cliente deletado com sucesso"}



def criar_investimento(db: Session, investimento):
    inv = Investimento(**investimento.dict())
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return inv



def listar_investimentos(db: Session):
    return db.query(Investimento).all()
