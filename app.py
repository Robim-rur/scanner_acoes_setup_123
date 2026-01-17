import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Scanner Ações B3 – Setup 1-2-3",
    layout="wide"
)

st.title("📈 Scanner Ações B3 – Setup 1-2-3 de Compra")
st.write("""
**Objetivo:** identificar automaticamente ações da B3 que deram  
**sinal de compra pelo padrão 1-2-3**, alinhado com tendência (EMA 69)  
e confirmação por **volume**.
""")

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================
def calcular_ema69(df):
    df["EMA69"] = ta.ema(df["Close"], length=69)
    return df

def tendencia_semanal_ok(df_diario):
    df_semanal = df_diario.resample("W").last()
    df_semanal = calcular_ema69(df_semanal)
    if len(df_semanal) < 70:
        return False
    return df_semanal["Close"].iloc[-1] > df_semanal["EMA69"].iloc[-1]

def identificar_setup_123(df):
    """
    Retorna True se o último candle fechou com sinal 1-2-3 de compra
    """
    if len(df) < 5:
        return False

    c1 = df.iloc[-3

