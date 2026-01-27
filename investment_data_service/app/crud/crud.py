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

    if cliente.patrimonio_total < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O patrimônio total não pode ser negativo"
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
    
    if db.query(Investimento).filter(Investimento.cliente_id == cliente_id).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível deletar o cliente pois existem investimentos associados a ele"
        )
    if patrimonio_total := getattr(cliente, 'patrimonio_total', 0) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível deletar o cliente pois ele possui patrimônio investido"
        )
    
    db.delete(cliente)
    db.commit()
    return {"mensagem": "Cliente deletado com sucesso"}



def criar_investimento(db: Session, investimento: InvestimentoCreate):
    investimento_db = Investimento(
        cliente_id=investimento.cliente_id,
        tipo_investimento=investimento.tipo_investimento,
        valor_investido=investimento.valor_investido,
        rentabilidade=investimento.rentabilidade,
        ativo=investimento.ativo
    )

    if not db.query(Cliente).filter(Cliente.id == investimento.cliente_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente associado ao investimento não encontrado"
        )
    
    if investimento.rentabilidade <= 0 or investimento.rentabilidade > 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A rentabilidade não pode ser negativa, zero ou maior que 1"
        )
    
    if investimento.valor_investido <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O valor investido não pode ser negativo ou zero"
        )

    
    db.add(investimento_db)
    db.commit()
    db.refresh(investimento_db)
    return investimento_db



def listar_investimentos(db: Session):
    return db.query(Investimento).all()

def listar_investimento_por_id(db: Session, investimento_id: str):
    return db.query(Investimento).filter(Investimento.id == investimento_id).first()

def atualizar_investimento(db: Session, investimento_id: str, dados_atualizados: dict):
    investimento = db.query(Investimento).filter(Investimento.id == investimento_id).first()
    if not investimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investimento não encontrado"
        )
    
    if 'rentabilidade' in dados_atualizados:
        rentabilidade = dados_atualizados['rentabilidade']
        if rentabilidade <= 0 or rentabilidade > 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A rentabilidade não pode ser negativa, zero ou maior que 1"
            )
    if 'valor_investido' in dados_atualizados:
        valor_investido = dados_atualizados['valor_investido']
        if valor_investido < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O valor investido não pode ser negativo"
            )
        
    for key, value in dados_atualizados.items():
        setattr(investimento, key, value)
    db.commit()
    db.refresh(investimento)
    return investimento

def deletar_investimento(db: Session, investimento_id: str):
    investimento = db.query(Investimento).filter(Investimento.id == investimento_id).first()
    if not investimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investimento não encontrado"
        )
    
    if investimento.ativo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível deletar o investimento pois ele está ativo"
        )
    db.delete(investimento)
    db.commit()
    return {"mensagem": "Investimento deletado com sucesso"}
