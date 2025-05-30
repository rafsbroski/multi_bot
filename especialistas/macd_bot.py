import pandas as pd
import logging

def analisar_sinal(df):
    try:
        df = pd.DataFrame(df)
        if df.empty or 'close' not in df.columns:
            return False

        df['EMA12'] = df['close'].ewm(span=12, adjust=False).mean()
        df['EMA26'] = df['close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['EMA12'] - df['EMA26']
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

        return df['MACD'].iloc[-1] > df['Signal'].iloc[-1]
    except Exception as e:
        logging.error(f"especialista_macd: {e}")
        return False