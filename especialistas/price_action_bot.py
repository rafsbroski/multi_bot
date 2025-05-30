import pandas as pd
import logging

def analisar_sinal(candles):
    try:
        df = pd.DataFrame(candles)
        if df.empty or df.shape[0] < 3:
            return False

        df['high'] = pd.to_numeric(df['high'], errors='coerce')
        df['low'] = pd.to_numeric(df['low'], errors='coerce')

        ultimo = df.iloc[-1]
        penultimo = df.iloc[-2]

        return ultimo['high'] > penultimo['high'] and ultimo['low'] > penultimo['low']
    except Exception as e:
        logging.error(f"especialista_price_action: {e}")
        return False