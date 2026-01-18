import yfinance as yf
import pandas as pd
import numpy as np


# ================= CONFIG =================
LOOKBACK_123 = 8 # janela para procurar o padrão
EMA_PERIOD = 69


# Lista completa de ativos (exemplo – mantenha sua lista completa aqui)
ativos = [
"PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA",
# ... COLE AQUI OS 173 ATIVOS SEM CORTAR O COLCHETE
]


# ================= FUNÇÕES =================


def ema(series, period):
return series.ewm(span=period, adjust=False).mean()




def is_inside_bar(df, i):
return (
df['High'].iloc[i] < df['High'].iloc[i - 1] and
df['Low'].iloc[i] > df['Low'].iloc[i - 1]
)




def detect_123(df):
"""
Detecta padrão 1-2-3 comprado dentro da janela LOOKBACK_123
Retorna:
- 'CLÁSSICO'
- 'INSIDE BAR'
- None
"""
for i in range(-LOOKBACK_123, -2):
low1 = df['Low'].iloc[i]
low2 = df['Low'].iloc[i + 1]
low3 = df['Low'].iloc[i + 2]


# Estrutura 1-2-3
if low2 < low1 and low3 > low2:
# Verifica rompimento ou inside bar
if df['Close'].iloc[i + 2] > df['High'].iloc[i + 1]:
return "CLÁSSICO"
elif is_inside_bar(df, i + 2):
return "INSIDE BAR"


return None


# ================= SCANNER =================


resultados = []


for ticker in ativos:
try:
df = yf.download(ticker, period="6mo", interval="1d", progress=False)
if len(df) < 100:
continue


# EMA 69 Diário
df['EMA69'] = ema(df['Close'], EMA_PERIOD)
cond_diario = df['Close'].iloc[-1] > df['EMA69'].iloc[-1]


# EMA 69 Semanal
df_week = df.resample('W').last()
df_week['EMA69'] = ema(df_week['Close'], EMA_PERIOD)
cond_semanal = df_week['Close'].iloc[-1] > df_week['EMA69'].iloc[-1]


if not (cond_diario and cond_semanal):
continue


setup = detect_123(df)
if setup:
resultados.append({
'Ativo': ticker,
'Setup': setup
})


except Exception as e:
print(f"Erro em {ticker}: {e}")


# ================= SAÍDA =================


resultado_df = pd.DataFrame(resultados)
print(resultado_df)
print(f"Total de sinais: {len(resultado_df)}")
# ===============================
# BDRs (50)
# ===============================
bdrs_50 = [
"AAPL34.SA","AMZO34.SA","GOGL34.SA","MSFT34.SA","TSLA34.SA","META34.SA",
"NFLX34.SA","NVDC34.SA","MELI34.SA","BABA34.SA","DISB34.SA","PYPL34.SA",
"JNJB34.SA","PGCO34.SA","KOCH34.SA","VISA34.SA","WMTB34.SA","NIKE34.SA",
"ADBE34.SA","AVGO34.SA","CSCO34.SA","COST34.SA","CVSH34.SA","GECO34.SA",
"GSGI34.SA","HDCO34.SA","INTC34.SA","JPMC34.SA","MAEL34.SA","MCDP34.SA",
"MDLZ34.SA","MRCK34.SA","ORCL34.SA","PEP334.SA","PFIZ34.SA","PMIC34.SA",
"QCOM34.SA","SBUX34.SA","TGTB34.SA","TMOS34.SA","TXN34.SA","UNHH34.SA",
"UPSB34.SA","VZUA34.SA","ABTT34.SA","AMGN34.SA","AXPB34.SA","BAOO34.SA",
"CATP34.SA","HONB34.SA"
]

# ===============================
# ETFs + FIIs (24)
# ===============================
etfs_fiis_24 = [
"BOVA11.SA","IVVB11.SA","SMAL11.SA","HASH11.SA","GOLD11.SA",
"GARE11.SA","HGLG11.SA","XPLG11.SA","VILG11.SA","BRCO11.SA",
"BTLG11.SA","XPML11.SA","VISC11.SA","HSML11.SA","MALL11.SA",
"KNRI11.SA","JSRE11.SA","PVBI11.SA","HGRE11.SA","MXRF11.SA",
"KNCR11.SA","KNIP11.SA","CPTS11.SA","IRDM11.SA"
]

# ===============================
# FUNÇÕES AUXILIARES
# ===============================
def ema(series, period=69):
    return series.ewm(span=period, adjust=False).mean()

def inside_bar(candle_atual, candle_anterior):
    return (
        candle_atual["High"] <= candle_anterior["High"] and
        candle_atual["Low"] >= candle_anterior["Low"]
    )

# ===============================
# SETUP 123 + INSIDE BAR
# (não limitado aos 3 últimos candles)
# ===============================
def setup_123_inside(df_d, df_w):
    if len(df_d) < 80 or len(df_w) < 80:
        return None

    df_d = df_d.copy()
    df_w = df_w.copy()

    df_d["EMA69"] = ema(df_d["Close"])
    df_w["EMA69"] = ema(df_w["Close"])

    # Tendência
    if df_d["Close"].iloc[-1] < df_d["EMA69"].iloc[-1]:
        return None
    if df_w["Close"].iloc[-1] < df_w["EMA69"].iloc[-1]:
        return None

    # Varre últimos 20 candles procurando estrutura
    for i in range(-20, -2):
        c1 = df_d.iloc[i-2]
        c2 = df_d.iloc[i-1]
        c3 = df_d.iloc[i]

        cond_123 = (
            c2["Low"] < c1["Low"] and
            c3["Low"] > c2["Low"]
        )

        cond_inside = inside_bar(c3, c2)

        if cond_123 or cond_inside:
            return {
                "Entrada": round(c3["High"], 2),
                "Stop": round(c2["Low"], 2),
                "Padrão": "Inside Bar" if cond_inside else "Setup 123"
            }

    return None
# ===============================
# BDRs (50)
# ===============================
bdrs_50 = [
"AAPL34.SA","AMZO34.SA","GOGL34.SA","MSFT34.SA","TSLA34.SA","META34.SA",
"NFLX34.SA","NVDC34.SA","MELI34.SA","BABA34.SA","DISB34.SA","PYPL34.SA",
"JNJB34.SA","PGCO34.SA","KOCH34.SA","VISA34.SA","WMTB34.SA","NIKE34.SA",
"ADBE34.SA","AVGO34.SA","CSCO34.SA","COST34.SA","CVSH34.SA","GECO34.SA",
"GSGI34.SA","HDCO34.SA","INTC34.SA","JPMC34.SA","MAEL34.SA","MCDP34.SA",
"MDLZ34.SA","MRCK34.SA","ORCL34.SA","PEP334.SA","PFIZ34.SA","PMIC34.SA",
"QCOM34.SA","SBUX34.SA","TGTB34.SA","TMOS34.SA","TXN34.SA","UNHH34.SA",
"UPSB34.SA","VZUA34.SA","ABTT34.SA","AMGN34.SA","AXPB34.SA","BAOO34.SA",
"CATP34.SA","HONB34.SA"
]

# ===============================
# ETFs + FIIs (24)
# ===============================
etfs_fiis_24 = [
"BOVA11.SA","IVVB11.SA","SMAL11.SA","HASH11.SA","GOLD11.SA",
"GARE11.SA","HGLG11.SA","XPLG11.SA","VILG11.SA","BRCO11.SA",
"BTLG11.SA","XPML11.SA","VISC11.SA","HSML11.SA","MALL11.SA",
"KNRI11.SA","JSRE11.SA","PVBI11.SA","HGRE11.SA","MXRF11.SA",
"KNCR11.SA","KNIP11.SA","CPTS11.SA","IRDM11.SA"
]

# ===============================
# FUNÇÕES AUXILIARES
# ===============================
def ema(series, period=69):
    return series.ewm(span=period, adjust=False).mean()

def inside_bar(candle_atual, candle_anterior):
    return (
        candle_atual["High"] <= candle_anterior["High"] and
        candle_atual["Low"] >= candle_anterior["Low"]
    )

# ===============================
# SETUP 123 + INSIDE BAR
# (não limitado aos 3 últimos candles)
# ===============================
def setup_123_inside(df_d, df_w):
    if len(df_d) < 80 or len(df_w) < 80:
        return None

    df_d = df_d.copy()
    df_w = df_w.copy()

    df_d["EMA69"] = ema(df_d["Close"])
    df_w["EMA69"] = ema(df_w["Close"])

    # Tendência
    if df_d["Close"].iloc[-1] < df_d["EMA69"].iloc[-1]:
        return None
    if df_w["Close"].iloc[-1] < df_w["EMA69"].iloc[-1]:
        return None

    # Varre últimos 20 candles procurando estrutura
    for i in range(-20, -2):
        c1 = df_d.iloc[i-2]
        c2 = df_d.iloc[i-1]
        c3 = df_d.iloc[i]

        cond_123 = (
            c2["Low"] < c1["Low"] and
            c3["Low"] > c2["Low"]
        )

        cond_inside = inside_bar(c3, c2)

        if cond_123 or cond_inside:
            return {
                "Entrada": round(c3["High"], 2),
                "Stop": round(c2["Low"], 2),
                "Padrão": "Inside Bar" if cond_inside else "Setup 123"
            }

    return None
