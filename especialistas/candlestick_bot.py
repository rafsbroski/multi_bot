import pandas as pd
import logging

def analisar_candle(candles, par):
    try:
        if not isinstance(candles, list) or len(candles) == 0:
            raise ValueError("Candles: lista vazia ou inválida.")
        
        # Deteta se os elementos são listas ou dicionários
        if all(isinstance(c, list) for c in candles):
            df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close"])
        elif all(isinstance(c, dict) for c in candles):
            df = pd.DataFrame(candles)
            df = df[["timestamp", "open", "high", "low", "close"]]
        else:
            raise ValueError("Formato inválido dos candles recebidos.")

        df["high"] = pd.to_numeric(df["high"], errors="coerce")
        df["low"] = pd.to_numeric(df["low"], errors="coerce")
        df["open"] = pd.to_numeric(df["open"], errors="coerce")
        df["close"] = pd.to_numeric(df["close"], errors="coerce")

        if df[["open", "high", "low", "close"]].isnull().any().any():
            raise ValueError("Valores nulos após conversão dos candles.")

        corpo = abs(df["close"].iloc[-1] - df["open"].iloc[-1])
        pavio_sup = df["high"].iloc[-1] - max(df["close"].iloc[-1], df["open"].iloc[-1])
        pavio_inf = min(df["close"].iloc[-1], df["open"].iloc[-1]) - df["low"].iloc[-1]

        if corpo < pavio_sup and corpo < pavio_inf:
            return "indefinido"
        elif df["close"].iloc[-1] > df["open"].iloc[-1]:
            return "compra"
        else:
            return "venda"

    except Exception as e:
        logging.error(f"especialista_candle: {str(e)}")
        return "indefinido"