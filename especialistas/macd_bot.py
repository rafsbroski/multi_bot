import pandas as pd
import logging

def analisar_macd(candles, par):
    try:
        # Validação da estrutura dos candles
        if not candles or not isinstance(candles, list) or len(candles) < 30:
            logging.error(f"[especialista_macd] DataFrame inválido ou com menos de 30 candles para {par}.")
            return None

        df = pd.DataFrame(candles)

        # Verifica se contém todas as colunas necessárias
        colunas_necessarias = {"timestamp", "open", "high", "low", "close", "volume"}
        if not colunas_necessarias.issubset(df.columns):
            logging.error(f"[especialista_macd] Estrutura de candles inválida ou insuficiente para {par}.")
            return None

        # Converte valores de 'close' para número
        df['close'] = pd.to_numeric(df['close'], errors='coerce')
        if df['close'].isnull().any():
            logging.error(f"[especialista_macd] Valores 'close' inválidos para {par}.")
            return None

        # Calcula MACD
        df['ema12'] = df['close'].ewm(span=12, adjust=False).mean()
        df['ema26'] = df['close'].ewm(span=26, adjust=False).mean()
        df['macd'] = df['ema12'] - df['ema26']
        df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()

        # Verifica cruzamento MACD
        macd_atual = df['macd'].iloc[-1]
        signal_atual = df['signal'].iloc[-1]
        macd_anterior = df['macd'].iloc[-2]
        signal_anterior = df['signal'].iloc[-2]

        if macd_anterior < signal_anterior and macd_atual > signal_atual:
            return "long"
        elif macd_anterior > signal_anterior and macd_atual < signal_atual:
            return "short"
        else:
            return None

    except Exception as e:
        logging.error(f"[especialista_macd] Erro ao analisar MACD para {par}: {e}")
        return None