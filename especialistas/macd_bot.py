import pandas as pd
import logging

def analisar_sinal(df):
    try:
        df = pd.DataFrame(df)
        df['close'] = pd.to_numeric(df['close'], errors='coerce')
        df.dropna(inplace=True)

        df['EMA12'] = df['close'].ewm(span=12, adjust=False).mean()
        df['EMA26'] = df['close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['EMA12'] - df['EMA26']
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

        if df['MACD'].iloc[-1] > df['Signal'].iloc[-1] and df['MACD'].iloc[-2] < df['Signal'].iloc[-2]:
            return 'compra'

        if df['MACD'].iloc[-1] < df['Signal'].iloc[-1] and df['MACD'].iloc[-2] > df['Signal'].iloc[-2]:
            return 'venda'

        return None

    except Exception as e:
        logging.error(f"[ERRO] especialista_macd: {e}")
        return None