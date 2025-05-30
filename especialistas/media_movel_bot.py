import pandas as pd
import logging

def analisar_sinal(candles):
    try:
        if not isinstance(candles, list) or not candles:
            raise ValueError("Candles: lista vazia ou inválida.")

        df = pd.DataFrame(candles)
        if df.empty or 'close' not in df.columns:
            raise ValueError("DataFrame vazio ou sem coluna 'close'.")

        df['MA20'] = df['close'].rolling(window=20).mean()

        if df['close'].iloc[-1] > df['MA20'].iloc[-1] and df['close'].iloc[-2] <= df['MA20'].iloc[-2]:
            return 'compra'
        elif df['close'].iloc[-1] < df['MA20'].iloc[-1] and df['close'].iloc[-2] >= df['MA20'].iloc[-2]:
            return 'venda'
        else:
            return None

    except Exception as e:
        logging.error(f"especialista_media_movel: {e}")
        return None