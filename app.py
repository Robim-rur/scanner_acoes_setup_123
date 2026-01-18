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
# LISTA DE ATIVOS
# =====================================================
ativos_scan = [
    "BOVV11.SA","BPAC11.SA","BRAX11.SA","BRSR6.SA","CPTS11.SA","CXSE3.SA",
    "DIVO11.SA","ITUB4.SA","KNRI11.SA","LOGG3.SA","MULT3.SA","NDIV11.SA",
    "PVBI11.SA","SPUB11.SA",
    "ABEV3.SA","ALPA4.SA","ARZZ3.SA","ASAI3.SA","BBAS3.SA","BBDC4.SA",
    "BRAP4.SA","CCRO3.SA","CMIG4.SA","CSAN3.SA","CSNA3.SA","EGIE3.SA",
    "ELET3.SA","PETR4.SA","VALE3.SA","WEGE3.SA"
]

# =====================================================
# FUNÇÃO DE DETECÇÃO DO SETUP
# =====================================================
def buscar_setup(df_d, df_w):
    if len(df_d) < 100 or len(df_w) < 100:
        return None

    df_d = df_d.copy()
    df_w = df_w.copy()

    df_d["EMA69"] = ta.ema(df_d["Close"], length=69)
    df_w["EMA69"] = ta.ema(df_w["Close"], length=69)

    # ============================
    # FILTRO DE TENDÊNCIA
    # ============================

    # EMA diária inclinada para cima
    if df_d["EMA69"].iloc[-1] <= df_d["EMA69"].iloc[-5]:
        return None

    # Preço acima da EMA 69 no semanal
    if df_w["Close"].iloc[-1] <= df_w["EMA69"].iloc[-1]:
        return None

    preco_atual = df_d["Close"].iloc[-1]

    # ============================
    # BUSCA DO PADRÃO (20 candles)
    # ============================
    for i in range(-20, -1):
        try:
            c3 = df_d.iloc[i]
            c2 = df_d.iloc[i - 1]
            c1 = df_d.iloc[i - 2]

            cond_123 = (
                c2["Low"] < c1["Low"] and
                c3["Low"] > c2["Low"]
            )

            cond_inside = (
                c3["High"] <= c2["High"] and
                c3["Low"] >= c2["Low"]
            )

            if cond_123 or cond_inside:
                entrada = round(max(c2["High"], c3["High"]), 2)
                stop = round(c2["Low"], 2)

                if preco_atual > stop:
                    return {
                        "Padrão": "123 Compra" if cond_123 else "Inside Bar",
                        "Preço Atual": round(preco_atual, 2),
                        "Entrada": entrada,
                        "Stop": stop,
                        "Distância (%)": round(((entrada / preco_atual) - 1) * 100, 2)
                    }
        except:
            continue

    return None

# =====================================================
# INTERFACE
# =====================================================
st.title("📈 Scanner Setup 123 + Inside Bar")
st.markdown("""
**Critérios**
- Compra somente  
- Tendência de alta pela **inclinação da EMA 69**
- Confirmação no semanal
- Inside Bar integrado ao 123
""")

st.info(f"🔎 Total de ativos escaneados: {len(ativos_scan)}")

# =====================================================
# EXECUÇÃO
# =====================================================
if st.button("▶️ Iniciar Scanner", key="scanner"):

    resultados = []
    barra = st.progress(0)

    dados_d = yf.download(ativos_scan, period="1y", interval="1d", group_by="ticker", progress=False)
    dados_w = yf.download(ativos_scan, period="3y", interval="1wk", group_by="ticker", progress=False)

    for i, ativo in enumerate(ativos_scan):
        try:
            df_d = dados_d[ativo].dropna()
            df_w = dados_w[ativo].dropna()

            sinal = buscar_setup(df_d, df_w)
            if sinal:
                sinal["Ativo"] = ativo.replace(".SA", "")
                resultados.append(sinal)
        except:
            pass

        barra.progress((i + 1) / len(ativos_scan))

    if resultados:
        df = pd.DataFrame(resultados)
        st.success(f"✅ {len(df)} sinais encontrados")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("❌ Nenhum ativo atendeu aos critérios.")
