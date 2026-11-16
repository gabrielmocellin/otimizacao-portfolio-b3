import json
from pathlib import Path

class LeitorAtivos:
    def __init__(self, caminho_arquivo: Path):
        self.caminho_arquivo = caminho_arquivo

    def carregar_tickers(self, quantidade_esperada: int = 5) -> list[str]:
        # 1. Verifica se o arquivo existe
        if not self.caminho_arquivo.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {self.caminho_arquivo}")

        # 2. Lê o JSON
        with open(self.caminho_arquivo, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        # 3. Verifica se a chave 'tickers' existe
        tickers = dados.get("tickers")
        
        if not tickers or not isinstance(tickers, list):
            raise ValueError("A chave 'tickers' não foi encontrada ou não é uma lista no JSON.")

        # 4. Verifica se há exatamente a quantidade esperada (ex: 5)
        if len(tickers) != quantidade_esperada:
            raise ValueError(f"Esperado {quantidade_esperada} tickers, mas foram encontrados {len(tickers)}.")

        # Retorna tudo em maiúsculo e sem espaços extras por segurança
        return [ticker.strip().upper() for ticker in tickers]
