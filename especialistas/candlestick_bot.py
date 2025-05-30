import pandas as pd
import logging

def analisar_sinal(df):
    try:
        df = pd.DataFrame(df)
        df['close'] = pd.to_numeric(df['close'], errors='coerce')
        df.dropna(inplace=True)

        df['body'] = df['close'] - df['open']
        df['range'] = df['high'] - df['low']
        df['upper_wick'] = df['high'] - df[['close', 'open']].max(axis=1)
        df['lower_wick'] = df[['close', 'open']].min(axis=1) - df['low']

        ultimo = df.iloc[-1]

        if (
            ultimo['body'] > 0 and
            ultimo['body'] > ultimo['upper_wick'] and
            ultimo['lower_wick'] > ultimo['body']
        ):
            return 'compra'

        if (
            ultimo['body'] < 0 and
            abs(ultimo['body']) > ultimo['lower_wick'] and
            ultimo['upper_wick'] > abs(ultimo['body'])
        ):
            return 'venda'

        return None

    except Exception as e:
        logging.error(f"[ERRO] especialista_candle: {e}")
        return None
