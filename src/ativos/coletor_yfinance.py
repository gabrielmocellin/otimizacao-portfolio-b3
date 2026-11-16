import pandas as pd
import yfinance as yf


class ColetorYFinance:
    def __init__(self, tickers: list[str]):
        # Garante que todos tenham o sufixo .SA para caracterizar a B3
        self.tickers_originais = tickers
        self.tickers_sa = [f"{t}.SA" if not t.endswith(".SA") else t for t in tickers]

    def obter_serie_historica(self, periodo: str = "1y", intervalo: str = "1d") -> pd.DataFrame:
        """
        Baixa os preços de fechamento ajustados para otimização e backtesting.
        """
        yf.enable_debug_mode()
        dados = yf.download(
            tickers=self.tickers_sa,
            period=periodo,
            interval=intervalo,
            auto_adjust=True,
            progress=False,
            threads=False # para não disparar múltiplas requisições simultâneas, evitando bloqueios do Yahoo Finance
        )

        # Seleciona apenas a coluna de fechamento
        precos = dados["Close"].copy()

        # Remove o sufixo '.SA' das colunas para manter os nomes limpos (ex: VALE3)
        precos.columns = [col.replace(".SA", "") for col in precos.columns]

        # Verifica se algum ativo veio totalmente vazio
        for ticker in self.tickers_originais:
            if ticker not in precos.columns or precos[ticker].dropna().empty:
                raise ValueError(f"Não foi possível obter histórico de preços para {ticker}.")

        return precos.dropna()

    def obter_fundamentos(self) -> pd.DataFrame:
        """
        Extrai indicadores fundamentalistas básicos de cada ativo.
        """
        lista_fundamentos = []

        for ticker_orig, ticker_sa in zip(self.tickers_originais, self.tickers_sa):
            ativo = yf.Ticker(ticker_sa)
            info = ativo.info

            # Coleta indicadores com .get() para evitar erro caso algum dado falte
            lista_fundamentos.append({
                "Ticker": ticker_orig,
                "Preco_Atual": info.get("currentPrice"),
                "P_L": info.get("trailingPE"),
                "P_VP": info.get("priceToBook"),
                "ROE": info.get("returnOnEquity"),
                "Dividend_Yield": info.get("dividendYield"),
                "Divida_Liquida_EBITDA": info.get("debtToEquity")
            })

        return pd.DataFrame(lista_fundamentos)
