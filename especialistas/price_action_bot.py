import pandas as pd

def analisar_sinal(df):
    try:
        df = pd.DataFrame(df)
        df['close'] = pd.to_numeric(df['close'], errors='coerce')
        df['open'] = pd.to_numeric(df['open'], errors='coerce')

        candle_anterior = df.iloc[-2]
        candle_atual = df.iloc[-1]

        if candle_anterior['close'] < candle_anterior['open'] and candle_atual['close'] > candle_atual['open'] and candle_atual['close'] > candle_anterior['open']:
            return 'compra'
        elif candle_anterior['close'] > candle_anterior['open'] and candle_atual['close'] < candle_atual['open'] and candle_atual['close'] < candle_anterior['open']:
            return 'venda'
        else:
            return None
    except Exception as e:
        print(f"[ERRO] especialista_price_action: {e}")
        return None
