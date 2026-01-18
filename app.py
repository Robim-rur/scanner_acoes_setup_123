import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta

# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================
st.set_page_config(
    page_title="Scanner Setup 123 + Inside Bar",
    layout="wide"
)

# =====================================================
# FUNÇÃO AUXILIAR
# =====================================================
def calcular_ema(series, periodo):
    return series.ewm(span=periodo, adjust=False).mean()

# =====================================================
# LISTAS DE ATIVOS (173)
# =====================================================
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
"BOVA11.SA","IVVB11.SA","SMAL11.SA","HASH11.SA","GOLD11.SA",
"GARE11.SA","HGLG11.SA","XPLG11.SA","VILG11.SA","BRCO11.SA",
"BTLG11.SA","XPML11.SA","VISC11.SA","HSML11.SA","MALL11.SA",
"KNRI11.SA","JSRE11.SA","PVBI11.SA","HGRE11.SA","MXRF11.SA",
"KNCR11.SA","KNIP11.SA","CPTS11.SA","IRDM11.SA"
]

# =====================================================
# SETUP 123 COM INSIDE BAR COMO CANDLE 3
# =====================================================
def setup_123(df_d, df_w):

    if len(df_d) < 100 or len(df_w) < 100:
        return None

    df_d["EMA69"] = calcular_ema(df_d["Close"], 69)
    df_w["EMA69"] = calcular_ema(df_w["Close"], 69)

    # EMA como ZONA de 3%
    if df_d["Close"].iloc[-1] < df_d["EMA69"].iloc[-1] * 0.97:
        return None

    if df_w["Close"].iloc[-1] < df_w["EMA69"].iloc[-1] * 0.97:
        return None

    # Procura padrão nos últimos 30 candles
    for i in range(-30, -2):

        c1 = df_d.iloc[i - 2]
        c2 = df_d.iloc[i - 1]
        c3 = df_d.iloc[i]

        # Candle 2 = fundo mais baixo
        if c2["Low"] < c1["Low"]:

            # Candle 3 normal OU inside bar
            cond_c3 = (
                c3["Low"] > c2["Low"] or
                (c3["High"] <= c2["High"] and c3["Low"] >= c2["Low"])
            )

            if cond_c3:
                return {
                    "Entrada": round(c3["High"], 2),
                    "Stop": round(c2["Low"], 2)
                }

    return None

# =====================================================
# FUNÇÃO DE VARREDURA
# =====================================================
def scan_lista(lista, tipo):
    resultados = []
    total = len(lista)

    barra = st.progress(0)
    status = st.empty()

    for i, ativo in enumerate(lista):
        status.text(f"Escaneando {i+1} de {total} ativos ({tipo})")
        barra.progress((i+1)/total)

        try:
            df_d = yf.download(ativo, period="1y", interval="1d", progress=False)
            df_w = yf.download(ativo, period="3y", interval="1wk", progress=False)

            if df_d.empty or df_w.empty:
                continue

            sinal = setup_123(df_d, df_w)

            if sinal:
                resultados.append({
                    "Ativo": ativo.replace(".SA", ""),
                    "Tipo": tipo,
                    "Entrada": sinal["Entrada"],
                    "Stop": sinal["Stop"]
                })

        except:
            continue

    return resultados

# =====================================================
# INTERFACE
# =====================================================
st.title("📈 Scanner Setup 123 + Inside Bar (EMA 69)")

total_ativos = len(acoes_100) + len(bdrs_50) + len(etfs_fiis_24)
st.info(f"🔎 Total de ativos escaneados: {total_ativos}")

if st.button("▶️ Iniciar Scanner Geral", key="scanner_geral"):

    resultados = []
    resultados += scan_lista(acoes_100, "AÇÃO")
    resultados += scan_lista(bdrs_50, "BDR")
    resultados += scan_lista(etfs_fiis_24, "ETF / FII")

    if resultados:
        st.success(f"✅ {len(resultados)} sinais encontrados")
        st.dataframe(pd.DataFrame(resultados), use_container_width=True)
    else:
        st.warning("❌ Nenhum ativo atendeu aos critérios no momento.")
