import pandas as pd
import logging

def analisar_sinal(candles):
    try:
        df = pd.DataFrame(candles)
        if df.empty or len(df.columns) < 5:
            raise ValueError("Candlestick: candles inválidos ou incompletos.")

        df.columns = ["timestamp", "open", "high", "low", "close"]
        df["high"] = pd.to_numeric(df["high"])
        df["low"] = pd.to_numeric(df["low"])

        corpo = abs(df["close"].iloc[-1] - df["open"].iloc[-1])
        pavio_superior = df["high"].iloc[-1] - max(df["close"].iloc[-1], df["open"].iloc[-1])
        pavio_inferior = min(df["close"].iloc[-1], df["open"].iloc[-1]) - df["low"].iloc[-1]

        if corpo < pavio_superior and corpo < pavio_inferior:
            return "indefinido"
        elif df["close"].iloc[-1] > df["open"].iloc[-1]:
            return "compra"
        else:
            return "venda"
    except Exception as e:
        logging.error(f"especialista_candle: {str(e)}")
        return "indefinido"