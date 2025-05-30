import pandas as pd

def analisar_sinal(df):
    try:
        df = pd.DataFrame(df)
        df['close'] = pd.to_numeric(df['close'], errors='coerce')

        df['EMA9'] = df['close'].ewm(span=9, adjust=False).mean()
        df['EMA21'] = df['close'].ewm(span=21, adjust=False).mean()

        if df['EMA9'].iloc[-2] < df['EMA21'].iloc[-2] and df['EMA9'].iloc[-1] > df['EMA21'].iloc[-1]:
            return 'compra'
        elif df['EMA9'].iloc[-2] > df['EMA21'].iloc[-2] and df['EMA9'].iloc[-1] < df['EMA21'].iloc[-1]:
            return 'venda'
        else:
            return None
    except Exception as e:
        print(f"[ERRO] especialista_media_movel: {e}")
        return None