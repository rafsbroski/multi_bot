import pandas as pd
import logging

def analisar_sinal(candles):
    try:
        if not isinstance(candles, list) or not candles:
            raise ValueError("Candles: lista vazia ou inválida.")

        df = pd.DataFrame(candles)
        if df.empty or not {'open', 'close', 'high', 'low'}.issubset(df.columns):
            raise ValueError("DataFrame malformado ou colunas ausentes.")

        candle = df.iloc[-1]
        corpo = abs(candle['close'] - candle['open'])
        sombra_total = candle['high'] - candle['low']

        if corpo > sombra_total * 0.7:
            if candle['close'] > candle['open']:
                return 'compra'
            elif candle['close'] < candle['open']:
                return 'venda'

        return None

    except Exception as e:
        logging.error(f"especialista_price_action: {e}")
        return None