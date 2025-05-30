import pandas as pd
import logging

def analisar_sinal(candles):
    try:
        df = pd.DataFrame(candles)
        if df.empty or df.shape[0] < 21:
            return False

        df['close'] = pd.to_numeric(df['close'], errors='coerce')
        mm_curta = df['close'].rolling(window=9).mean()
        mm_longa = df['close'].rolling(window=21).mean()

        return mm_curta.iloc[-1] > mm_longa.iloc[-1] and mm_curta.iloc[-2] < mm_longa.iloc[-2]
    except Exception as e:
        logging.error(f"especialista_media_movel: {e}")
        return False