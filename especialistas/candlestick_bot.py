import pandas as pd
import logging

def analisar_sinal(candles):
    try:
        df = pd.DataFrame(candles)
        if df.empty or df.shape[0] < 3:
            return False

        df['close'] = pd.to_numeric(df['close'], errors='coerce')
        df['open'] = pd.to_numeric(df['open'], errors='coerce')

        condicao_martelo = (
            (df['close'].iloc[-1] > df['open'].iloc[-1]) and
            ((df['open'].iloc[-1] - df['low'].iloc[-1]) > 2 * (df['close'].iloc[-1] - df['open'].iloc[-1]))
        )
        return condicao_martelo
    except Exception as e:
        logging.error(f"especialista_candle: {e}")
        return False