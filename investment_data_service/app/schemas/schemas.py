from pydantic import BaseModel
from datetime import datetime

class ClienteCreate(BaseModel):
    nome: str
    cpf: str
    email: str
    perfil_investidor: str
    patrimonio_total: float

class ClienteResponse(ClienteCreate):
    id: str
    data_cadastro: datetime

class InvestimentoCreate(BaseModel):
    cliente_id: str
    tipo_investimento: str
    valor_investido: float
    rentabilidade: float
    ativo: bool