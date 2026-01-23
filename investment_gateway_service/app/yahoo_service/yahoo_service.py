import yfinance as yf

def obter_preco(ticker: str):
    try:
        ativo = yf.Ticker(ticker)
        hist = ativo.history(period="1d")

        if hist.empty:
            return {
                "erro": "Ticker inválido ou sem dados no momento"
            }

        preco = float(hist["Close"].iloc[-1])
        return {
            "ticker": ticker,
            "preco_atual": preco
        }

    except Exception as e:
        return {
            "erro": "Falha ao consultar Yahoo Finance",
            "detalhe": str(e)
        }
