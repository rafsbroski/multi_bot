import pandas as pd
import logging

def analisar_sinal(candles):
    try:
        df = pd.DataFrame(candles)
        if df.empty or df.shape[0] < 15:
            return False

        df['close'] = pd.to_numeric(df['close'], errors='coerce')
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        return rsi.iloc[-1] < 30
    except Exception as e:
        logging.error(f"especialista_rsi: {e}")
        return False