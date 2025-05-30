import pandas as pd
import logging

def analisar_sinal(candles):
    try:
        if not isinstance(candles, list) or len(candles) < 25:
            raise ValueError("Estrutura de candles inválida ou insuficiente.")

        df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["close"] = pd.to_numeric(df["close"], errors="coerce")

        df["ma9"] = df["close"].rolling(window=9).mean()
        df["ma21"] = df["close"].rolling(window=21).mean()

        if df["ma9"].iloc[-1] > df["ma21"].iloc[-1] and df["ma9"].iloc[-2] <= df["ma21"].iloc[-2]:
            return "compra"
        elif df["ma9"].iloc[-1] < df["ma21"].iloc[-1] and df["ma9"].iloc[-2] >= df["ma21"].iloc[-2]:
            return "venda"
        else:
            return None

    except Exception as e:
        logging.error(f"especialista_media_movel: {e}")
        return None