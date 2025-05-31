import pandas as pd
import logging

def analisar_media_movel(candles, par):
    try:
        if not candles:
            logging.error(f"[especialista_media_movel] Lista de candles vazia para {par}.")
            return None

        logging.debug(f"[especialista_media_movel] Candles recebidos para {par}: {candles[:3]}")  # debug real

        candles_validos = [c for c in candles if isinstance(c, (list, tuple)) and len(c) >= 6]
        if len(candles_validos) < 50:
            logging.error(f"[especialista_media_movel] Candles com dados incompletos para {par}. Tamanho: {len(candles_validos)}")
            return None

        df = pd.DataFrame(candles_validos[:100], columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume'
        ])

        df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].apply(pd.to_numeric, errors='coerce')

        if df.isnull().values.any():
            logging.error(f"[especialista_media_movel] Valores inválidos no DataFrame para {par}.")
            return None

        df['ma20'] = df['close'].rolling(window=20).mean()
        df['ma50'] = df['close'].rolling(window=50).mean()

        if df[['ma20', 'ma50']].isnull().any().any():
            return None

        if df['ma20'].iloc[-1] > df['ma50'].iloc[-1] and df['ma20'].iloc[-2] <= df['ma50'].iloc[-2]:
            return "long"
        elif df['ma20'].iloc[-1] < df['ma50'].iloc[-1] and df['ma20'].iloc[-2] >= df['ma50'].iloc[-2]:
            return "short"
        return None

    except Exception as e:
        logging.exception(f"[especialista_media_movel] Erro ao analisar sinal para {par}: {str(e)}")
        return None