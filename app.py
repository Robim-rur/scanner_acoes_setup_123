import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Scanner Geral – Setup 1-2-3 de Compra",
    layout="wide"
)

st.title("📈 Scanner Geral — Setup 1-2-3 de Compra")

# =========================================================
# LISTAS DE ATIVOS
# =========================================================

acoes_lista = [
    "PETR4.SA","VALE3.SA","ITUB4.SA","BBDC4.SA","BBAS3.SA","ABEV3.SA","JBSS3.SA","ELET3.SA","WEGE3.SA","RENT3.SA",
    "ITSA4.SA","HAPV3.SA","GGBR4.SA","SUZB3.SA","B3SA3.SA","MGLU3.SA","LREN3.SA","EQTL3.SA","CSAN3.SA","RDOR3.SA",
    "RAIL3.SA","PRIO3.SA","VIBR3.SA","UGPA3.SA","SBSP3.SA","ASAI3.SA","CCRO3.SA","RADL3.SA","CMIG4.SA","CPLE6.SA",
    "TOTS3.SA","CPFE3.SA","ENEV3.SA","EMBR3.SA","BRFS3.SA","CRFB3.SA","MULT3.SA","CSNA3.SA","GOAU4.SA","USIM5.SA",
    "HYPE3.SA","FLRY3.SA","EGIE3.SA","TAEE11.SA","TRPL4.SA","KLBN11.SA","BPAC11.SA","SANB11.SA","PSSA3.SA","BBSE3.SA",
    "MRVE3.SA","CYRE3.SA","EZTC3.SA","DIRR3.SA","ALPA4.SA","YDUQ3.SA","COGN3.SA","AZUL4.SA","GOLL4.SA","CVCB3.SA",
    "TIMS3.SA","VIVT3.SA","BRAP4.SA","CMIN3.SA","CSMG3.SA","SAPR11.SA","ALUP11.SA","AURE3.SA","SMTO3.SA","SLCE3.SA",
    "BEEF3.SA","MRFG3.SA","MDIA3.SA","STBP3.SA","ARZZ3.SA","VIVA3.SA","SOMA3.SA","GMAT3.SA","LWSA3.SA","CASH3.SA",
    "POSI3.SA","INTB3.SA","RECV3.SA","BRKM5.SA","DXCO3.SA","POMO4.SA","TUPY3.SA","KEPL3.SA","RANI3.SA","UNIP6.SA"
]

ativos_lista = [
    "BOVA11.SA","IVVB11.SA","SMAL11.SA","HASH11.SA","SPXI11.SA","TECB11.SA","NASD11.SA","GOLD11.SA",
    "DIVO11.SA","PIBB11.SA","BOVV11.SA","BBOV11.SA","B5P211.SA",
    "GARE11.SA","HGLG11.SA","XPLG11.SA","VILG11.SA","BRCO11.SA","BTLG11.SA","XPML11.SA","VISC11.SA",
    "HSML11.SA","MALL11.SA","KNRI11.SA","JSRE11.SA","PVBI11.SA","HGRE11.SA","BRCR11.SA","RBRP11.SA",
    "ALZR11.SA","GGRC11.SA"
]

bdrs_top = [
    "AAPL34.SA","AMZO34.SA","GOGL34.SA","MSFT34.SA","TSLA34.SA","META34.SA","NFLX34.SA","NVDC34.SA","MELI34.SA","BABA34.SA",
    "DISB34.SA","PYPL34.SA","JNJB34.SA","PGCO34.SA","HOME34.SA","COCA34.SA","MCDC34.SA","NIKE34.SA","NUBR33.SA","VZBO34.SA",
    "BERK34.SA","JPMC34.SA","VISA34.SA","WMTB34.SA","XOMP34.SA","ORCL34.SA","PEP34.SA","PFIZ34.SA","SBUB34.SA","TGTB34.SA"
]

# =========================================================
# FUNÇÃO SETUP 1-2-3 (SEM VOLUME)
# =========================================================
def setup_123(df):
    if len(df) < 5:
        return None

    c1 = df.iloc[-4]
    c2 = df.iloc[-3]  # fundo mais baixo
    c3 = df.iloc[-2]

    if not (c2["Low"] < c1["Low"] and c3["Low"] > c2["Low"]):
        return None

    observacao = ""
    if c3["Low"] > c2["Low"] and c3["High"] > c2["High"]:
        observacao = "Candle 3 com mínima e máxima maiores que o candle 2"

    return {
        "Entrada": round(c3["High"], 2),
        "Stop": round(c2["Low"], 2),
        "Observação": observacao
    }

# =========================================================
# SCANNER
# =========================================================
def scan(lista, tipo):
    resultados = []
    total = len(lista)

    barra = st.progress(0)
    status = st.empty()

    for i, ativo in enumerate(lista):
        status.text(f"Escaneando {i+1} de {total} ativos...")
        barra.progress((i+1)/total)

        try:
            df = yf.download(ativo, period="6mo", interval="1d", progress=False)
            if df.empty:
                continue

            sinal = setup_123(df)
            if sinal:
                resultados.append({
                    "Ativo": ativo.replace(".SA",""),
                    "Tipo": tipo,
                    **sinal
                })
        except:
            pass

    return resultados

# =========================================================
# EXECUÇÃO
# =========================================================
if st.button("▶️ Iniciar Scanner Geral"):
    resultados = []
    resultados += scan(acoes_lista, "AÇÃO")
    resultados += scan(ativos_lista, "ETF / FII")
    resultados += scan(bdrs_top, "BDR")

    if resultados:
        st.dataframe(pd.DataFrame(resultados))
    else:
        st.warning("Nenhum ativo encontrou o setup 1-2-3 hoje.")
