import streamlit as st
import pandas as pd
import yfinance as yf

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Scanner Geral – Setup 1-2-3 de Compra",
    layout="wide"
)

st.title("📈 Scanner Geral — Setup 1-2-3 de Compra")

# =========================================================
# LISTAS UNIFICADAS (BASE DE 173 ATIVOS)
# =========================================================

acoes_100 = [
    "RRRP3.SA","ALOS3.SA","ALPA4.SA","ABEV3.SA","ARZZ3.SA","ASAI3.SA","AZUL4.SA","B3SA3.SA","BBAS3.SA","BBDC3.SA",
    "BBDC4.SA","BBSE3.SA","BEEF3.SA","BPAC11.SA","BRAP4.SA","BRFS3.SA","BRKM5.SA","CCRO3.SA","CMIG4.SA","CMIN3.SA",
    "COGN3.SA","CPFE3.SA","CPLE6.SA","CRFB3.SA","CSAN3.SA","CSNA3.SA","CYRE3.SA","DXCO3.SA","EGIE3.SA","ELET3.SA",
    "ELET6.SA","EMBR3.SA","ENEV3.SA","ENGI11.SA","EQTL3.SA","EZTC3.SA","FLRY3.SA","GGBR4.SA","GOAU4.SA","GOLL4.SA",
    "HAPV3.SA","HYPE3.SA","ITSA4.SA","ITUB4.SA","JBSS3.SA","KLBN11.SA","LREN3.SA","LWSA3.SA","MGLU3.SA","MRFG3.SA",
    "MRVE3.SA","MULT3.SA","NTCO3.SA","PETR3.SA","PETR4.SA","PRIO3.SA","RADL3.SA","RAIL3.SA","RAIZ4.SA","RENT3.SA",
    "RECV3.SA","SANB11.SA","SBSP3.SA","SLCE3.SA","SMTO3.SA","SUZB3.SA","TAEE11.SA","TIMS3.SA","TOTS3.SA","TRPL4.SA",
    "UGPA3.SA","USIM5.SA","VALE3.SA","VIVT3.SA","VIVA3.SA","WEGE3.SA","YDUQ3.SA","AURE3.SA","BHIA3.SA","CASH3.SA",
    "CVCB3.SA","DIRR3.SA","ENAT3.SA","GMAT3.SA","IFCM3.SA","INTB3.SA","JHSF3.SA","KEPL3.SA","MOVI3.SA","ORVR3.SA",
    "PETZ3.SA","PLAS3.SA","POMO4.SA","POSI3.SA","RANI3.SA","RAPT4.SA","STBP3.SA","TEND3.SA","TUPY3.SA"
]

bdrs_50 = [
    "AAPL34.SA","AMZO34.SA","GOGL34.SA","MSFT34.SA","TSLA34.SA","META34.SA","NFLX34.SA","NVDC34.SA","MELI34.SA","BABA34.SA",
    "DISB34.SA","PYPL34.SA","JNJB34.SA","PGCO34.SA","KOCH34.SA","VISA34.SA","WMTB34.SA","NIKE34.SA","ADBE34.SA","AVGO34.SA",
    "CSCO34.SA","COST34.SA","CVSH34.SA","GECO34.SA","GSGI34.SA","HDCO34.SA","INTC34.SA","JPMC34.SA","MAEL34.SA","MCDP34.SA",
    "MDLZ34.SA","MRCK34.SA","ORCL34.SA","PEP334.SA","PFIZ34.SA","PMIC34.SA","QCOM34.SA","SBUX34.SA","TGTB34.SA","TMOS34.SA",
    "TXN34.SA","UNHH34.SA","UPSB34.SA","VZUA34.SA","ABTT34.SA","AMGN34.SA","AXPB34.SA","BAOO34.SA","CATP34.SA","HONB34.SA"
]

etfs_fiis_24 = [
    "BOVA11.SA","IVVB11.SA","SMAL11.SA","HASH11.SA","GOLD11.SA","GARE11.SA","HGLG11.SA","XPLG11.SA","VILG11.SA","BRCO11.SA",
    "BTLG11.SA","XPML11.SA","VISC11.SA","HSML11.SA","MALL11.SA","KNRI11.SA","JSRE11.SA","PVBI11.SA","HGRE11.SA","MXRF11.SA",
    "KNCR11.SA","KNIP11.SA","CPTS11.SA","IRDM11.SA"
]

# =========================================================
# CONTROLE DE TOTAL DE ATIVOS
# =========================================================
total_ativos = len(acoes_100) + len(bdrs_50) + len(etfs_fiis_24)
st.info(f"🔢 Total de ativos no scanner: {total_ativos}")

# =========================================================
# FUNÇÃO SETUP 1-2-3 DE COMPRA (SEM VOLUME)
# =========================================================
def setup_123_compra(df):
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
# FUNÇÃO DE VARREDURA
# =========================================================
def scan(lista, tipo):
    resultados = []
    total = len(lista)

    barra = st.progress(0)
    status = st.empty()

    for i, ativo in enumerate(lista):
        status.text(f"Escaneando {i+1} de {total} ativos...")
        barra.progress((i+1) / total)

        try:
            df = yf.download(ativo, period="6mo", interval="1d", progress=False)
            if df.empty:
                continue

            sinal = setup_123_compra(df)
            if sinal:
                resultados.append({
                    "Ativo": ativo.replace(".SA", ""),
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
    resultados += scan(acoes_100, "AÇÃO")
    resultados += scan(etfs_fiis_24, "ETF / FII")
    resultados += scan(bdrs_50, "BDR")

    if resultados:
        st.dataframe(pd.DataFrame(resultados))
    else:
        st.warning("Nenhum ativo encontrou o setup 1-2-3 hoje.")

