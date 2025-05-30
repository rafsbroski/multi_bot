import pandas as pd
import logging

def analisar_sinal(candles):
    try:
        df = pd.DataFrame(candles)
        if df.empty or df.shape[0] < 26:
            return False

        df['close'] = pd.to_numeric(df['close'], errors='coerce')
        ema12 = df['close'].ewm(span=12, adjust=False).mean()
        ema26 = df['close'].ewm(span=26, adjust=False).mean()
        macd = ema12 - ema26
        sinal = macd.ewm(span=9, adjust=False).mean()

        return macd.iloc[-1] > sinal.iloc[-1] and macd.iloc[-2] < sinal.iloc[-2]
    except Exception as e:
        logging.error(f"especialista_macd: {e}")
        return False