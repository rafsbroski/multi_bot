import pandas as pd
import logging

def analisar_sinal(candles):
    try:
        df = pd.DataFrame(candles)
        if df.empty or len(df.columns) < 5:
            raise ValueError("PriceAction: candles inválidos ou incompletos.")

        df.columns = ["timestamp", "open", "high", "low", "close"]
        df["close"] = pd.to_numeric(df["close"])

        if df["close"].iloc[-1] > df["close"].iloc[-2] > df["close"].iloc[-3]:
            return "compra"
        elif df["close"].iloc[-1] < df["close"].iloc[-2] < df["close"].iloc[-3]:
            return "venda"
        else:
            return "indefinido"
    except Exception as e:
        logging.error(f"especialista_price_action: {str(e)}")
        return "indefinido"