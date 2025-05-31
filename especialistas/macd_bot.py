import pandas as pd
import logging

def analisar_candle(candles, par):
    try:
        if not candles or len(candles) < 26:
            logging.error("[especialista_macd] Estrutura de candles inválida ou insuficiente.")
            return None

        df = pd.DataFrame(candles)
        if df.shape[1] < 5:
            logging.error("[especialista_macd] Estrutura de DataFrame inválida.")
            return None

        df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        df['close'] = pd.to_numeric(df['close'], errors='coerce')

        if df['close'].isnull().any():
            logging.error("[especialista_macd] Valores inválidos na coluna 'close'.")
            return None

        exp1 = df['close'].ewm(span=12, adjust=False).mean()
        exp2 = df['close'].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()

        if macd.iloc[-1] > signal.iloc[-1] and macd.iloc[-2] <= signal.iloc[-2]:
            return "long"
        elif macd.iloc[-1] < signal.iloc[-1] and macd.iloc[-2] >= signal.iloc[-2]:
            return "short"
        else:
            return None

    except Exception as e:
        logging.exception(f"[especialista_macd] Erro ao analisar sinal: {str(e)}")
        return None