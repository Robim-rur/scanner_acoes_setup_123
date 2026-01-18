import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Scanner B3 - Setup 1-2-3",
    layout="wide"
)

# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================
def calcular_ema(df, periodo):
    return ta.ema(df["Close"], length=periodo)

def analisar_ativo(ticker, tipo):
    try:
        df = yf.download(
            ticker,
            period="2y",
            interval="1d",
            progress=False
        )

        if df is None or len(df) < 120:
            return None

        df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]

        # EMA 69 diária
        df["EMA69_D"] = calcular_ema(df, 69)

        # Dados semanais
        df_w = df.resample("W").last()
        df_w["EMA69_W"] = calcular_ema(df_w, 69)

        # Últimos candles
        c1 = df.iloc[-3]
        c2 = df.iloc[-2]
        c3 = df.iloc[-1]
        w = df_w.iloc[-1]

        # ============================
        # SETUP 1-2-3 (REGRA PRINCIPAL)
        # ============================
        estrutura_ok = (
            c2["Low"] < c1["Low"] and
            c3["Low"] > c2["Low"]
        )

        if not estrutura_ok:
            return None

        rompimento_ok = c3["Close"] > c3["High"] * 0.999
        if not rompimento_ok:
            return None

        if c3["Close"] <= c3["EMA69_D"]:
            return None

        if w["Close"] <= w["EMA69_W"]:
            return None

        if c3["Volume"] <= c2["Volume"]:
            return None

        # ============================
        # OBSERVAÇÃO (NÃO EXCLUDENTE)
        # ============================
        candle3_dominante = (
            c3["Low"] > c2["Low"] and
            c3["High"] > c2["High"]
        )

        observacao = (
            "Candle 3 dominante (mín + máx maiores)"
            if candle3_dominante
            else "Candle 3 padrão / possível inside bar"
        )

        return {
            "ATIVO": ticker.replace(".SA", ""),
            "TIPO": tipo,
            "PREÇO": round(float(c3["Close"]), 2),
            "EMA69_D": round(float(c3["EMA69_D"]), 2),
            "EMA69_W": round(float(w["EMA69_W"]), 2),
            "VOLUME C3": int(c3["Volume"]),
            "VOLUME C2": int(c2["Volume"]),
            "OBSERVAÇÃO": observacao
        }

    except Exception:
        return None

# =========================================================
# INTERFACE STREAMLIT
# =========================================================
def main():
    st.title("📈 Scanner B3 — Setup 1-2-3 de Compra")

    st.write("""
    **Critérios automáticos:**
    - Setup 1-2-3 (3 candles)
    - Preço acima da EMA 69 diária
    - Tendência confirmada pela EMA 69 semanal
    - Volume do Candle 3 maior que o Candle 2

    **Observação informativa:**
    - Candle 3 dominante (mín + máx maiores) ou padrão
    """)

    # ============================
    # LISTAS DE ATIVOS
    # ============================
    acoes = [
        "PETR4.SA","VALE3.SA","ITUB4.SA","BBDC4.SA","BBAS3.SA","ABEV3.SA","WEGE3.SA","RENT3.SA",
        "B3SA3.SA","LREN3.SA","EQTL3.SA","PRIO3.SA","RADL3.SA","EGIE3.SA","PSSA3.SA","BBSE3.SA"
    ]

    bdrs = [
        "AAPL34.SA","AMZO34.SA","GOGL34.SA","MSFT34.SA","TSLA34.SA","META34.SA","NFLX34.SA",
        "NVDC34.SA","MELI34.SA","BABA34.SA","VISA34.SA","WMTB34.SA","ORCL34.SA","PEP34.SA"
    ]

    fiis = [
        "HGLG11.SA","XPLG11.SA","BTLG11.SA","XPML11.SA","VISC11.SA","KNRI11.SA","BRCR11.SA",
        "ALZR11.SA","GGRC11.SA"
    ]

    etfs = [
        "BOVA11.SA","IVVB11.SA","SMAL11.SA","NASD11.SA","GOLD11.SA","DIVO11.SA","B5P211.SA"
    ]

    ativos = []
    tipos = {}

    for a in acoes:
        ativos.append(a)
        tipos[a] = "AÇÃO"

    for b in bdrs:
        ativos.append(b)
        tipos[b] = "BDR"

    for f in fiis:
        ativos.append(f)
        tipos[f] = "FII"

    for e in etfs:
        ativos.append(e)
        tipos[e] = "ETF"

    if st.button("🔍 Iniciar Scanner"):
        resultados = []
        barra = st.progress(0)
        status = st.empty()

        for i, ativo in enumerate(ativos):
            status.text(f"Analisando {ativo.replace('.SA','')}...")
            r = analisar_ativo(ativo, tipos[ativo])
            if r:
                resultados.append(r)
            barra.progress((i + 1) / len(ativos))

        status.success("Varredura concluída")

        if resultados:
            st.dataframe(pd.DataFrame(resultados))
        else:
            st.info("Nenhum ativo gerou sinal pelo Setup 1-2-3 hoje.")

# =========================================================
if __name__ == "__main__":
    main()




