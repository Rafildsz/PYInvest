from pydantic import BaseModel
from datetime import datetime

class ClienteCreate(BaseModel):
    nome: str
    cpf: str
    email: str
    perfil_investidor: str
    patrimonio_total: float

class ClienteUpdate(BaseModel):
    nome: str
    email: str 
    perfil_investidor: str 
    patrimonio_total: float 

class ClienteResponse(ClienteCreate):
    id: str
    data_cadastro: datetime
    
    class Config:
        orm_mode = True

class InvestimentoCreate(BaseModel):
    cliente_id: str
    tipo_investimento: str
    valor_investido: float
    rentabilidade: float
    ativo: bool

class InvestimentoUpdate(BaseModel):
    tipo_investimento: str
    valor_investido: float
    rentabilidade: float
    ativo: bool 

class InvestimentoResponse(InvestimentoCreate):
    id: str
    data_aplicacao: datetime
    
    class Config:
        orm_mode = True