import pandas as pd
import logging

def analisar_macd(candles, par):
    try:
        if not candles:
            logging.error(f"[especialista_macd] Lista de candles vazia para {par}.")
            return None

        logging.debug(f"[especialista_macd] Candles recebidos para {par}: {candles[:3]}")

        if not isinstance(candles[0], dict):
            logging.error(f"[especialista_macd] Formato inválido dos candles para {par}. Esperado dicionário.")
            return None

        df = pd.DataFrame(candles)

        if not {'open', 'high', 'low', 'close', 'volume'}.issubset(df.columns):
            logging.error(f"[especialista_macd] Campos essenciais em falta nos candles para {par}.")
            return None

        df = df[['open', 'high', 'low', 'close', 'volume']].copy()
        df = df.apply(pd.to_numeric, errors='coerce')

        if df.isnull().values.any() or len(df) < 30:
            logging.error(f"[especialista_macd] DataFrame inválido ou com menos de 30 candles para {par}.")
            return None

        ema12 = df['close'].ewm(span=12, adjust=False).mean()
        ema26 = df['close'].ewm(span=26, adjust=False).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()

        if macd.iloc[-1] > signal.iloc[-1] and macd.iloc[-2] <= signal.iloc[-2]:
            return "long"
        elif macd.iloc[-1] < signal.iloc[-1] and macd.iloc[-2] >= signal.iloc[-2]:
            return "short"
        return None

    except Exception as e:
        logging.exception(f"[especialista_macd] Erro ao analisar sinal para {par}: {str(e)}")
        return None