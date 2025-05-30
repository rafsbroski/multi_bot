import pandas as pd
import logging

def analisar_sinal(candles):
    try:
        if not isinstance(candles, list) or not candles:
            raise ValueError("Candles: lista vazia ou inválida.")

        df = pd.DataFrame(candles)
        if df.empty or 'close' not in df.columns:
            raise ValueError("DataFrame vazio ou sem coluna 'close'.")

        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        df['RSI'] = 100 - (100 / (1 + rs))

        rsi = df['RSI'].iloc[-1]
        if rsi < 30:
            return 'compra'
        elif rsi > 70:
            return 'venda'
        else:
            return None

    except Exception as e:
        logging.error(f"especialista_rsi: {e}")
        return None