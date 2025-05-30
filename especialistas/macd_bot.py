import pandas as pd

def macd_strategy(df):
    short_ema = df['close'].ewm(span=12, adjust=False).mean()
    long_ema = df['close'].ewm(span=26, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=9, adjust=False).mean()

    if macd.iloc[-1] > signal.iloc[-1] and macd.iloc[-2] <= signal.iloc[-2]:
        return 'buy'
    elif macd.iloc[-1] < signal.iloc[-1] and macd.iloc[-2] >= signal.iloc[-2]:
        return 'sell'
    else:
        return 'hold'

def analisar(df):
    try:
        if len(df) < 35:
            return 'hold'
        return macd_strategy(df)
    except:
        return 'hold'