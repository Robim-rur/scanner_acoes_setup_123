import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Scanner Ações B3 - Setup 1-2-3",
    layout="wide"
)

# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================
def calcular_ema(df, periodo):
    return ta.ema(df["Close"], length=periodo)

def analisar_ativo(ticker):
    try:
        # -------------------------------------------------
        # DADOS DIÁRIOS
        # -------------------------------------------------
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

        # -------------------------------------------------
        # DADOS SEMANAIS
        # -------------------------------------------------
        df_w = df.resample("W").last()
        df_w["EMA69_W"] = calcular_ema(df_w, 69)

        # Últimos candles
        c1 = df.iloc[-3]  # Candle 1
        c2 = df.iloc[-2]  # Candle 2
        c3 = df.iloc[-1]  # Candle 3

        w = df_w.iloc[-1]

        # =================================================
        # SETUP 1-2-3 DE COMPRA
        # =================================================

        # 1️⃣ Estrutura 1-2-3
        estrutura_ok = (
            c2["Low"] < c1["Low"] and
            c3["Low"] > c2["Low"]
        )

        if not estrutura_ok:
            return None

        # 2️⃣ Rompimento da máxima do Candle 3
        rompimento_ok = c3["Close"] > c3["High"] * 0.999

        if not rompimento_ok:
            return None

        # 3️⃣ Filtro EMA 69 diária
        ema_diaria_ok = (
            c3["Close"] > c3["EMA69_D"]
        )

        if not ema_diaria_ok:
            return None

        # 4️⃣ Filtro EMA 69 semanal
        ema_semanal_ok = (
            w["Close"] > w["EMA69_W"]
        )

        if not ema_semanal_ok:
            return None

        # 5️⃣ Volume obrigatório (Candle 3 > Candle 2)
        volume_ok = c3["Volume"] > c2["Volume"]

        if not volume_ok:
            return None

        # =================================================
        # SE PASSOU EM TUDO → SINAL
        # =================================================
        return {
            "ATIVO": ticker.replace(".SA", ""),
            "PREÇO": round(float(c3["Close"]), 2),
            "EMA69_D": round(float(c3["EMA69_D"]), 2),
            "EMA69_W": round(float(w["EMA69_W"]), 2),
            "VOLUME C3": int(c3["Volume"]),
            "VOLUME C2": int(c2["Volume"])
        }

    except Exception:
        return None

# =========================================================
# INTERFACE STREAMLIT
# =========================================================
def main():
    st.title("📈 Scanner Ações B3 — Setup 1-2-3 de Compra")
    st.write(
        """
        **Critérios automáticos:**
        - Padrão 1-2-3 válido
        - Preço acima da EMA 69 diária
        - Tendência confirmada pela EMA 69 semanal
        - Volume do Candle 3 maior que o Candle 2
        """
    )

    # Universo de ativos (opção A)
    ativos = [
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

    if st.button("🔍 Iniciar Scanner"):
        resultados = []
        barra = st.progress(0)
        status = st.empty()

        for i, ativo in enumerate(ativos):
            status.text(f"Analisando {ativo.replace('.SA','')}...")
            r = analisar_ativo(ativo)
            if r:
                resultados.append(r)
            barra.progress((i + 1) / len(ativos))

        status.success("Varredura concluída")

        if resultados:
            st.dataframe(pd.DataFrame(resultados))
        else:
            st.info("Nenhuma ação gerou sinal pelo Setup 1-2-3 hoje.")

# =========================================================
if __name__ == "__main__":
    main()



