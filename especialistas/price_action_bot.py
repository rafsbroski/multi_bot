import pandas as pd
import logging

def analisar_sinal(df):
    try:
        df = pd.DataFrame(df)
        if df.empty or 'high' not in df.columns or 'low' not in df.columns or 'close' not in df.columns:
            return False

        candle_atual = df.iloc[-1]
        candle_anterior = df.iloc[-2]

        return (
            candle_anterior['low'] > candle_atual['low'] and
            candle_atual['close'] > candle_anterior['close']
        )
    except Exception as e:
        logging.error(f"especialista_price_action: {e}")
        return False
