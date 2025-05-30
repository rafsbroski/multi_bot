import pandas as pd
import logging

def analisar_sinal(candles):
    try:
        df = pd.DataFrame(candles)
        if df.empty or len(df.columns) < 5:
            raise ValueError("RSI: candles inválidos ou incompletos.")

        df.columns = ["timestamp", "open", "high", "low", "close"]
        df["close"] = pd.to_numeric(df["close"])
        delta = df["close"].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        if rsi.iloc[-1] < 30:
            return "compra"
        elif rsi.iloc[-1] > 70:
            return "venda"
        else:
            return "indefinido"
    except Exception as e:
        logging.error(f"especialista_rsi: {str(e)}")
        return "indefinido"