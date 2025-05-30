import pandas as pd
import logging

def analisar_sinal(df, periodo=14):
    try:
        df = pd.DataFrame(df)
        if df.empty or 'close' not in df.columns:
            return False

        delta = df['close'].diff()
        ganho = delta.clip(lower=0)
        perda = -delta.clip(upper=0)

        media_ganho = ganho.rolling(window=periodo).mean()
        media_perda = perda.rolling(window=periodo).mean()
        rs = media_ganho / media_perda
        rsi = 100 - (100 / (1 + rs))

        return rsi.iloc[-1] < 30
    except Exception as e:
        logging.error(f"especialista_rsi: {e}")
        return False