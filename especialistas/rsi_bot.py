import pandas as pd

def analisar_sinal(candles):
    df = pd.DataFrame(candles)
    df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    df['close'] = pd.to_numeric(df['close'])

    delta = df['close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    if rsi.iloc[-1] < 30:
        return "compra"
    elif rsi.iloc[-1] > 70:
        return "venda"
    else:
        return False