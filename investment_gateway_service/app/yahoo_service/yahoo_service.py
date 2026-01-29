import yfinance as yf
import pandas as pd

def obter_preco(ticker: str):
    try:
        ativo = yf.Ticker(ticker)
        hist = ativo.history(period="1d")

        if hist is None or hist.empty or "Close" not in hist.columns:
            return {
                "erro": "Ticker inválido ou sem dados no momento"
            }

        preco = float(hist["Close"].iloc[-1])
        return {
            "ticker": ticker,
            "preco_atual": preco
        }

    except (yf.shared._exceptions.YFQueryError, pd.errors.EmptyDataError, ValueError) as e:
        return {
            "erro": "Erro ao consultar dados do Yahoo Finance",
            "detalhe": str(e)
        }
    except Exception as e:
        return {
            "erro": "Falha inesperada ao consultar Yahoo Finance",
            "detalhe": str(e)
        }
    