def detectar_padrao(df):
    if len(df) < 3:
        return 'hold'

    c1 = df.iloc[-3]
    c2 = df.iloc[-2]
    c3 = df.iloc[-1]

    # Exemplo de martelo invertido
    if c3['close'] > c3['open'] and c3['low'] < c2['low'] and c3['high'] > c2['high']:
        return 'buy'
    elif c3['close'] < c3['open'] and c3['high'] > c2['high'] and c3['low'] < c2['low']:
        return 'sell'
    else:
        return 'hold'

def analisar(df):
    try:
        return detectar_padrao(df)
    except:
        return 'hold'