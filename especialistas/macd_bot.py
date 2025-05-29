import pandas as pd

def analisar_sinal(candles):
    df = pd.DataFrame(candles)
    df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    df['close'] = pd.to_numeric(df['close'])

    # Cálculo do MACD
    short_ema = df['close'].ewm(span=12, adjust=False).mean()
    long_ema = df['close'].ewm(span=26, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=9, adjust=False).mean()

    # Geração de sinal
    if macd.iloc[-2] < signal.iloc[-2] and macd.iloc[-1] > signal.iloc[-1]:
        return "compra"
    elif macd.iloc[-2] > signal.iloc[-2] and macd.iloc[-1] < signal.iloc[-1]:
        return "venda"
    else:
        return False