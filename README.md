# PYInvest

## Visão Geral

O **PYInvest** é um sistema de investimentos desenvolvido em Python, baseado em **arquitetura de microserviços**, que simula o funcionamento de um banco de investimentos moderno.  
O projeto integra **dados reais do mercado financeiro**, realiza **análises de carteira**, **projeções de retorno** e demonstra comunicação entre serviços via **APIs REST**.

---

## Objetivo do Projeto

Construir um ecossistema de microserviços capaz de:

- Gerenciar clientes investidores (CRUD)
- Gerenciar investimentos (CRUD)
- Consumir dados do mercado financeiro via **Yahoo Finance**
- Realizar análises financeiras e projeções de retorno
- Consolidar dados entre serviços via REST
- Aplicar boas práticas de arquitetura, validação e tratamento de erros

---

## Arquitetura do Sistema

O sistema é composto por **dois microserviços independentes**, porém integrados:

### INVESTMENT-DATA-SERVICE (Data Service)

Responsável pela persistência e validação dos dados do sistema.

### INVESTMENT-GATEWAY-SERVICE (API Gateway)

Este serviço atua como ponto único de entrada da aplicação.
Ele não persiste dados, sendo responsável por orquestrar chamadas, realizar cálculos e análises financeiras.

### Endpoints Públicos
---

GET    /api/v1/clientes

GET    /api/v1/clientes/{id}

POST   /api/v1/clientes

PUT    /api/v1/clientes/{id}

DELETE /api/v1/clientes/{id}

---

GET    /api/v1/investimentos

GET    /api/v1/investimentos/cliente/{cliente_id}

POST   /api/v1/investimentos

PUT    /api/v1/investimentos/{id}

DELETE /api/v1/investimentos/{id}

---

GET /api/v1/calculos/projecao/{cliente_id}

GET /api/v1/calculos/patrimonio/{cliente_id}

GET /api/v1/analises/carteira/{cliente_id}

GET /api/v1/analises/mercado/{ticker}

---

## Tecnologias Utilizadas

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- yfinance
- Pandas
- Requests
- Uvicorn

---

## Como Executar o Projeto

### Criar ambiente virtual

python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows

### Instalar dependências

pip install -r requirements.txt

### Executar os serviços

uvicorn app.main:app --reload --port 8001  # data service

uvicorn app.main:app --reload --port 8000  # gateway service



