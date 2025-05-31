import pandas as pd
import logging

def analisar_macd(candles, par):
    try:
        if not candles:
            logging.error(f"[especialista_macd] Lista de candles vazia para {par}.")
            return None

        logging.debug(f"[especialista_macd] Candles recebidos para {par}: {candles[:3]}")  # debug real

        candles_validos = [c for c in candles if isinstance(c, (list, tuple)) and len(c) >= 6]
        if len(candles_validos) < 30:
            logging.error(f"[especialista_macd] Candles com dados incompletos para {par}. Tamanho: {len(candles_validos)}")
            return None

        df = pd.DataFrame(candles_validos[:100], columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume'
        ])

        df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].apply(pd.to_numeric, errors='coerce')

        if df.isnull().values.any():
            logging.error(f"[especialista_macd] Valores inválidos no DataFrame para {par}.")
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