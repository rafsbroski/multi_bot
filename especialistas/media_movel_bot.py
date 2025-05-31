import pandas as pd
import logging

def analisar_sinal(candles):
    try:
        if not candles or len(candles) < 50:
            logging.error("[especialista_media_movel] Estrutura de candles inválida ou insuficiente.")
            return None

        df = pd.DataFrame(candles)
        if df.shape[1] < 5:
            logging.error("[especialista_media_movel] Estrutura de DataFrame inválida.")
            return None

        df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        df['close'] = pd.to_numeric(df['close'], errors='coerce')

        if df['close'].isnull().any():
            logging.error("[especialista_media_movel] Valores inválidos na coluna 'close'.")
            return None

        df['ma20'] = df['close'].rolling(window=20).mean()
        df['ma50'] = df['close'].rolling(window=50).mean()

        if df['ma20'].isnull().any() or df['ma50'].isnull().any():
            return None

        if df['ma20'].iloc[-1] > df['ma50'].iloc[-1] and df['ma20'].iloc[-2] <= df['ma50'].iloc[-2]:
            return "long"
        elif df['ma20'].iloc[-1] < df['ma50'].iloc[-1] and df['ma20'].iloc[-2] >= df['ma50'].iloc[-2]:
            return "short"
        else:
            return None

    except Exception as e:
        logging.exception(f"[especialista_media_movel] Erro ao analisar sinal: {str(e)}")
        return None