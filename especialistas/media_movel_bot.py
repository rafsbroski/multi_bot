import pandas as pd
import logging

def analisar_media_movel(candles, par):
    try:
        if not candles:
            logging.error(f"[especialista_media_movel] Lista de candles vazia para {par}.")
            return None

        if not isinstance(candles[0], dict):
            logging.error(f"[especialista_media_movel] Formato inválido dos candles para {par}. Esperado dicionário.")
            return None

        df = pd.DataFrame(candles)
        if not {'open', 'high', 'low', 'close', 'volume'}.issubset(df.columns):
            logging.error(f"[especialista_media_movel] Campos essenciais em falta nos candles para {par}.")
            return None

        df = df[['open', 'high', 'low', 'close', 'volume']].copy()
        df = df.apply(pd.to_numeric, errors='coerce')
        df.dropna(inplace=True)

        if len(df) < 60:
            logging.error(f"[especialista_media_movel] DataFrame inválido ou com menos de 60 candles válidos para {par}.")
            return None

        df['ma20'] = df['close'].rolling(window=20).mean()
        df['ma50'] = df['close'].rolling(window=50).mean()

        if df[['ma20', 'ma50']].iloc[-2:].isnull().any().any():
            logging.error(f"[especialista_media_movel] Médias móveis não estão completas nas últimas linhas para {par}.")
            return None

        if df['ma20'].iloc[-1] > df['ma50'].iloc[-1] and df['ma20'].iloc[-2] <= df['ma50'].iloc[-2]:
            return "long"
        elif df['ma20'].iloc[-1] < df['ma50'].iloc[-1] and df['ma20'].iloc[-2] >= df['ma50'].iloc[-2]:
            return "short"

        return None

    except Exception as e:
        logging.exception(f"[especialista_media_movel] Erro ao analisar sinal para {par}: {str(e)}")
        return None