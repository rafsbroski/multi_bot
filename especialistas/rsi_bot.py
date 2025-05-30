import pandas as pd

def rsi_strategy(df):
    window = 14
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    last_rsi = rsi.iloc[-1]

    if last_rsi < 30:
        return 'buy'
    elif last_rsi > 70:
        return 'sell'
    else:
        return 'hold'

def analisar(df):
    try:
        if len(df) < 15:
            return 'hold'
        return rsi_strategy(df)
    except:
        return 'hold'