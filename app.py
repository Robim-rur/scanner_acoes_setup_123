import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta

# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================
st.set_page_config(page_title="Scanner 1-2-3 Compra", layout="wide")

st.title("📈 Scanner Setup 1-2-3 de Compra (Long Only)")

st.write("""
**Critérios obrigatórios**
- Estrutura 1-2-3 de compra (3 candles)
- Candle 2 é o fundo mais baixo
- Candle 3 com fundo mais alto que o candle 2
- Preço acima da EMA 69 no diário
- Tendência confirmada pela EMA 69 no semanal

**Observação (não elimina sinal)**
- Candle 3 dominante (mínima e máxima acima do candle 2)
- Caso contrário: inside bar ou candle neutro
- Volume NÃO é critério
""")

# =====================================================
# LISTA COMPLETA DE ATIVOS (173)
# =====================================================
ativos = [
    # AÇÕES
    "PETR4.SA","VALE3.SA","ITUB4.SA","BBDC4.SA","BBAS3.SA","ABEV3.SA","JBSS3.SA","ELET3.SA","WEGE3.SA","RENT3.SA",
    "ITSA4.SA","HAPV3.SA","GGBR4.SA","SUZB3.SA","B3SA3.SA","MGLU3.SA","LREN3.SA","EQTL3.SA","CSAN3.SA","RDOR3.SA",
    "RAIL3.SA","PRIO3.SA","VIBR3.SA","UGPA3.SA","SBSP3.SA","ASAI3.SA","CCRO3.SA","RADL3.SA","CMIG4.SA","CPLE6.SA",
    "TOTS3.SA","CPFE3.SA","ENEV3.SA","EMBR3.SA","BRFS3.SA","CRFB3.SA","MULT3.SA","CSNA3.SA","GOAU4.SA","USIM5.SA",
    "HYPE3.SA","FLRY3.SA","EGIE3.SA","TAEE11.SA","TRPL4.SA","KLBN11.SA","BPAC11.SA","SANB11.SA","PSSA3.SA","BBSE3.SA",
    "MRVE3.SA","CYRE3.SA","EZTC3.SA","DIRR3.SA","ALPA4.SA","YDUQ3.SA","COGN3.SA","AZUL4.SA","GOLL4.SA","CVCB3.SA",
    "TIMS3.SA","VIVT3.SA","BRAP4.SA","CMIN3.SA","CSMG3.SA","SAPR11.SA","ALUP11.SA","AURE3.SA","SMTO3.SA","SLCE3.SA",
    "BEEF3.SA","MRFG3.SA","MDIA3.SA","STBP3.SA","ARZZ3.SA","VIVA3.SA","SOMA3.SA","GMAT3.SA","LWSA3.SA","CASH3.SA",
    "POSI3.SA","INTB3.SA","RECV3.SA","BRKM5.SA","DXCO3.SA","POMO4.SA","TUPY3.SA","KEPL3.SA","RANI3.SA","UNIP6.SA",

    # ETFs
    "BOVA11.SA","IVVB11.SA","SMAL11.SA","HASH11.SA","SPXI11.SA","TECB11.SA","NASD11.SA","GOLD11.SA",
    "DIVO11.SA","PIBB11.SA","BOVV11.SA","BBOV11.SA","B5P211.SA",

    # FIIs
    "GARE11.SA","HGLG11.SA","XPLG11.SA","VILG11.SA","BRCO11.SA","BTLG11.SA","XPML11.SA","VISC11.SA",
    "HSML11.SA","MALL11.SA","KNRI11.SA","JSRE11.SA","PVBI11.SA","HGRE11.SA","BRCR11.SA","RBRP11.SA",
    "ALZR11.SA","GGRC11.SA",

    # BDRs
    "AAPL34.SA","AMZO34.SA","GOGL34.SA","MSFT34.SA",]
# =========================================================
# EXECUÇÃO DO SCANNER
# =========================================================
if st.button("🔍 Iniciar Scanner"):
    resultados = []
    barra = st.progress(0)
    status = st.empty()
    contador = st.empty()

    total = len(ativos)

    for i, ativo in enumerate(ativos):
        status.text(f"Analisando {ativo.replace('.SA','')}...")
        r = analisar_ativo(ativo)
        if r:
            resultados.append(r)

        barra.progress((i + 1) / total)
        contador.markdown(f"**Ativos escaneados: {i+1} de {total}**")

    status.success("Varredura concluída")
    contador.markdown(f"**Total de ativos escaneados: {total}**")

    if resultados:
        st.dataframe(pd.DataFrame(resultados), use_container_width=True)
    else:
        st.info("Nenhum ativo gerou sinal hoje.")
# =========================================================
# EXECUÇÃO DO SCANNER
# =========================================================
if st.button("🔍 Iniciar Scanner"):
    resultados = []
    barra = st.progress(0)
    status = st.empty()
    contador = st.empty()

    total = len(ativos)

    for i, ativo in enumerate(ativos):
        status.text(f"Analisando {ativo.replace('.SA','')}...")
        r = analisar_ativo(ativo)
        if r:
            resultados.append(r)

        barra.progress((i + 1) / total)
        contador.markdown(f"**Ativos escaneados: {i+1} de {total}**")

    status.success("Varredura concluída")
    contador.markdown(f"**Total de ativos escaneados: {total}**")

    if resultados:
        st.dataframe(pd.DataFrame(resultados), use_container_width=True)
    else:
        st.info("Nenhum ativo gerou sinal hoje.")






