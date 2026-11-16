"""
Script Principal (main.py)
---------------------------------------------------
Projeto Prático: Avaliação Fundamentalista, Otimização de Portfólio e Backtesting
Disciplina: Matemática Financeira — UFPR

Preciso definir os critérios de corte (screening criteria) 
filtros objetivos utilizados pra reduzir um universo amplo de ativos (como todas as ações da B3) 
a uma lista enxuta de candidatas viáveis para análise aprofundada ou composição de carteira.

Executa sequencialmente:
- Etapa 1: Seleção e Triagem dos Ativos (Universo B3) e Coleta de Séries Temporais
"""

from pathlib import Path
from src.ativos.leitor_ativos import LeitorAtivos
from src.ativos.coletor_yfinance import ColetorYFinance

RAIZ_PROJETO = Path(__file__).resolve().parent
CAMINHO_JSON = RAIZ_PROJETO / "config" / "ativos.json"


def main():
    try:
        # 1. Lê e valida os tickers do JSON
        leitor = LeitorAtivos(CAMINHO_JSON)
        tickers = leitor.carregar_tickers(quantidade_esperada=5)
        print("Ativos validados:", tickers)

        # 2. Instancia o coletor e busca os dados
        coletor = ColetorYFinance(tickers)

        print("\nBaixando histórico de preços...")
        df_precos = coletor.obter_serie_historica(periodo="2y", intervalo="1mo")
        print(df_precos.tail())  # Mostra os últimos 5 dias

        print("\nColetando indicadores fundamentalistas...")
        df_fundamentos = coletor.obter_fundamentos()
        print(df_fundamentos)

    except (FileNotFoundError, ValueError) as erro:
        print(f"Erro na execução: {erro}")


if __name__ == "__main__":
    main()

