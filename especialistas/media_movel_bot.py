import pandas as pd
import logging

def analisar_sinal(df):
    try:
        df = pd.DataFrame(df)
        if df.empty or 'close' not in df.columns:
            return False

        df['MM20'] = df['close'].rolling(window=20).mean()
        return df['close'].iloc[-1] > df['MM20'].iloc[-1]
    except Exception as e:
        logging.error(f"especialista_media_movel: {e}")
        return False