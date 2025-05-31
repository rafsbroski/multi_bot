import pandas as pd
import logging

def analisar_macd(candles, par):
    try:
        if not candles or len(candles) < 30:
            logging.error(f"[especialista_macd] Estrutura de candles inválida ou insuficiente para {par}.")
            return None

        candles_validos = [c for c in candles if isinstance(c, (list, tuple)) and len(c) >= 5]
        if len(candles_validos) < 30:
            logging.error(f"[especialista_macd] Candles com dados incompletos para {par}.")
            return None

        df = pd.DataFrame(candles_validos[:100], columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume'
        ])
        df['close'] = pd.to_numeric(df['close'], errors='coerce')

        if df['close'].isnull().any():
            logging.error(f"[especialista_macd] Valores inválidos na coluna 'close' para {par}.")
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