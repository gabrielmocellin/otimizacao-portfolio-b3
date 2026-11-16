import json
from pathlib import Path
import streamlit as st
from src.ativos.leitor_ativos import LeitorAtivos
from src.ativos.coletor_yfinance import ColetorYFinance

# Configuração inicial da página
st.set_page_config(
    page_title="Análise de Portfólio - B3",
    page_icon="📈",
    layout="wide"
)

RAIZ_PROJETO = Path(__file__).resolve().parent
CAMINHO_JSON = RAIZ_PROJETO / "config" / "ativos.json"


# Cache evita baixar do Yahoo Finance toda vez que você clicar em um botão
# Atualmente o padrão de armazenamento é 1 hora (3600 segundos) (ttl)
@st.cache_data(ttl=3600, show_spinner="Coletando dados no Yahoo Finance...")
# O período e o intervalo são passados como parâmetros para permitir flexibilidade na coleta de dados,
# por padrão coloquei o período de 1 ano e intervalo mensal, mas você pode alterar conforme necessário.
def carregar_dados_mercado(tickers: list[str], periodo: str = "1y", intervalo: str = "1mo"):
    coletor = ColetorYFinance(tickers)
    df_precos = coletor.obter_serie_historica(periodo=periodo, intervalo=intervalo)
    df_fundamentos = coletor.obter_fundamentos()
    return df_precos, df_fundamentos

# Tenho que trocar isso depois, mas por enquanto é uma função simples que lê o JSON e retorna a lista de dicionários com os detalhes das teses.
# depende do formato do JSON, mas assumindo que ele tem uma chave "detalhes" que contém a lista de dicionários.
def carregar_teses_json(caminho: Path) -> list[dict]:
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f).get("detalhes", [])

# Função principal que organiza a execução do Streamlit, incluindo a coleta de dados e a renderização das abas.
def main():
    st.title("📈 Avaliação Fundamentalista e Portfólio (B3)")
    st.markdown("Painel interativo dos 5 ativos selecionados por setor econômico.")

    # Barra lateral para controles e filtros
    with st.sidebar:
        st.header("⚙️ Configurações")
        periodo = st.selectbox(
            "Janela Histórica",
            options=["6mo", "1y", "2y", "5y"],
            index=2  # Padrão: 2y (começa selecionado na terceira opção da lista)
        )
        intervalo = st.selectbox(
            "Intervalo de Tempo",
            options=["1d", "1wk", "1mo"],
            index=2  # Padrão: 1mo (começa selecionado na terceira opção da lista)
        )
        if st.button("🔄 Atualizar Dados Agora"):
            st.cache_data.clear()
            st.rerun()

    try:
        # 1. Usa sua classe existente para ler e validar o JSON
        leitor = LeitorAtivos(CAMINHO_JSON)
        tickers = leitor.carregar_tickers(quantidade_esperada=5)
        detalhes_setores = carregar_teses_json(CAMINHO_JSON)

        # 2. Busca os dados (usando cache)
        df_precos, df_fundamentos = carregar_dados_mercado(tickers, periodo, intervalo)

        # 3. Organiza a visualização em abas limpas
        aba_fundamentos, aba_precos, aba_teses = st.tabs([
            "📊 Indicadores Fundamentalistas",
            "📈 Histórico de Preços",
            "🏢 Tese por Setor"
        ])

        with aba_fundamentos:
            st.subheader("Múltiplos e Rentabilidade")
            st.dataframe(
                df_fundamentos,
                use_container_width=True,
                hide_index=True
            )

        with aba_precos:
            st.subheader(f"Evolução dos Preços Ajustados ({periodo})")
            
            # Normaliza base 100 para comparar ativos com preços diferentes no mesmo gráfico
            normalizar = st.checkbox("Normalizar preços (Base 100) para comparar rentabilidade", value=True)
            
            if normalizar:
                df_grafico = (df_precos / df_precos.iloc[0]) * 100
            else:
                df_grafico = df_precos

            st.line_chart(df_grafico)

            with st.expander("Ver tabela completa de cotações diárias"):
                st.dataframe(df_precos.sort_index(ascending=False), use_container_width=True)

        with aba_teses:
            st.subheader("Justificativa Econômica dos Ativos")
            for item in detalhes_setores:
                with st.container(border=True):
                    st.markdown(f"**{item['ticker']} — {item['empresa']}** | *{item['setor_economico']} ({item['segmento']})*")
                    st.write(item["tese"])

    except (FileNotFoundError, ValueError) as erro:
        st.error(f"Erro ao carregar os dados: {erro}")


if __name__ == "__main__":
    main()
