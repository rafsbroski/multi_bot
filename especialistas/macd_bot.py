import pandas as pd
import logging

def analisar_sinal(candles):
    try:
        if not isinstance(candles, list) or not candles:
            raise ValueError("Candles: lista vazia ou inválida.")

        df = pd.DataFrame(candles)
        if df.empty or 'close' not in df.columns:
            raise ValueError("DataFrame vazio ou sem coluna 'close'.")

        df['EMA12'] = df['close'].ewm(span=12, adjust=False).mean()
        df['EMA26'] = df['close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['EMA12'] - df['EMA26']
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

        if df['MACD'].iloc[-1] > df['Signal'].iloc[-1] and df['MACD'].iloc[-2] <= df['Signal'].iloc[-2]:
            return 'compra'
        elif df['MACD'].iloc[-1] < df['Signal'].iloc[-1] and df['MACD'].iloc[-2] >= df['Signal'].iloc[-2]:
            return 'venda'
        else:
            return None

    except Exception as e:
        logging.error(f"especialista_macd: {e}")
        return None