import pandas as pd
import logging

def analisar_sinal(candles):
    try:
        df = pd.DataFrame(candles)
        if df.empty or len(df.columns) < 5:
            raise ValueError("MACD: candles inválidos ou incompletos.")

        df.columns = ["timestamp", "open", "high", "low", "close"]
        df["close"] = pd.to_numeric(df["close"])

        ema12 = df["close"].ewm(span=12, adjust=False).mean()
        ema26 = df["close"].ewm(span=26, adjust=False).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()

        if macd.iloc[-1] > signal.iloc[-1]:
            return "compra"
        elif macd.iloc[-1] < signal.iloc[-1]:
            return "venda"
        else:
            return "indefinido"
    except Exception as e:
        logging.error(f"especialista_macd: {str(e)}")
        return "indefinido"