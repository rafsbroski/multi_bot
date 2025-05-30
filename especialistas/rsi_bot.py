import pandas as pd
import logging

def analisar_sinal(df):
    try:
        df = pd.DataFrame(df)
        df['close'] = pd.to_numeric(df['close'], errors='coerce')
        df.dropna(inplace=True)

        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        if rsi.iloc[-1] < 30:
            return 'compra'

        if rsi.iloc[-1] > 70:
            return 'venda'

        return None

    except Exception as e:
        logging.error(f"[ERRO] especialista_rsi: {e}")
        return None