import pandas as pd
import logging

def analisar_sinal(candles):
    try:
        if not isinstance(candles, list) or len(candles) < 50:
            raise ValueError("Estrutura de candles inválida ou insuficiente.")

        df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])

        df["close"] = pd.to_numeric(df["close"], errors="coerce")
        df["ema12"] = df["close"].ewm(span=12, adjust=False).mean()
        df["ema26"] = df["close"].ewm(span=26, adjust=False).mean()
        df["macd"] = df["ema12"] - df["ema26"]
        df["signal"] = df["macd"].ewm(span=9, adjust=False).mean()

        if df["macd"].iloc[-1] > df["signal"].iloc[-1] and df["macd"].iloc[-2] <= df["signal"].iloc[-2]:
            return "compra"
        elif df["macd"].iloc[-1] < df["signal"].iloc[-1] and df["macd"].iloc[-2] >= df["signal"].iloc[-2]:
            return "venda"
        else:
            return None

    except Exception as e:
        logging.error(f"especialista_macd: {e}")
        return None