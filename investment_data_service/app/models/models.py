import uuid
from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.sqlite import BLOB
from datetime import datetime
from app.database.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String)
    cpf = Column(String, unique=True)
    email = Column(String)
    perfil_investidor = Column(String)
    patrimonio_total = Column(Float)
    data_cadastro = Column(DateTime, default=datetime.utcnow)

class Investimento(Base):
    __tablename__ = "investimentos"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    cliente_id = Column(String, ForeignKey("clientes.id"))
    tipo_investimento = Column(String)
    valor_investido = Column(Float)
    data_aplicacao = Column(DateTime, default=datetime.utcnow)
    rentabilidade = Column(Float)
    ativo = Column(Boolean)
