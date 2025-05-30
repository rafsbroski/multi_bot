import pandas as pd
import logging

def analisar_sinal(df):
    try:
        df = pd.DataFrame(df)
        if df.empty or 'open' not in df.columns or 'close' not in df.columns:
            return False

        ultima = df.iloc[-1]
        return ultima['close'] > ultima['open']
    except Exception as e:
        logging.error(f"especialista_candle: {e}")
        return False