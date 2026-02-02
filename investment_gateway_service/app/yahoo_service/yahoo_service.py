import yfinance as yf


def obter_dados_mercado(ticker: str, periodo="1mo"):
    ativo = yf.Ticker(ticker)
    hist = ativo.history(period=periodo)

    if hist.empty:
        raise ValueError("Sem dados")

    preco_atual = float(hist["Close"].iloc[-1])
    preco_inicial = float(hist["Close"].iloc[0])

    variacao_percentual = ((preco_atual - preco_inicial) / preco_inicial) * 100

    return {
        "ticker": ticker,
        "preco_atual": preco_atual,
        "variacao_percentual": round(variacao_percentual, 2),
        "periodo": periodo
    }
