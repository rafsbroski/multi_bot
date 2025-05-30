import pandas as pd
import logging

def analisar_sinal(candles):
    try:
        df = pd.DataFrame(candles)
        if df.empty or len(df.columns) < 5:
            raise ValueError("MM: candles inválidos ou incompletos.")

        df.columns = ["timestamp", "open", "high", "low", "close"]
        df["close"] = pd.to_numeric(df["close"])

        mm_curta = df["close"].rolling(window=9).mean()
        mm_longa = df["close"].rolling(window=21).mean()

        if mm_curta.iloc[-1] > mm_longa.iloc[-1]:
            return "compra"
        elif mm_curta.iloc[-1] < mm_longa.iloc[-1]:
            return "venda"
        else:
            return "indefinido"
    except Exception as e:
        logging.error(f"especialista_media_movel: {str(e)}")
        return "indefinido"