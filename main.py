import time
from datetime import datetime, date
from config import API_KEY, API_SECRET
import ccxt
from telegram_alerts import send_telegram_message
from especialistas.media_movel_bot import avaliar_media_movel
from especialistas.momentum_bot import avaliar_momentum
from especialistas.price_action_bot import avaliar_price_action
from especialistas.rsi_bot import avaliar_rsi
from especialistas.volume_bot import avaliar_volume

# ─── Inicialização do client CCXT para FUTURES PERPÉTUOS (swap) na MEXC ───
client = ccxt.mexc({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'enableRateLimit': True,
    'options': {'defaultType': 'swap'}
})
# Carrega mercados e valida símbolos
client.load_markets()
# (opcional) debug: confirma os market IDs
print("Market ID BTC/USDT →", client.markets['BTC/USDT']['id'])
print("Market ID ETH/USDT →", client.markets['ETH/USDT']['id'])
print("Market ID SOL/USDT →", client.markets['SOL/USDT']['id'])

INTERVALO = '5m'
# — CORREÇÃO: símbolos corretos para swap perpétuo —
PARES = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
ALAVANCAGEM = 50

MAX_TENTATIVAS = 3
DELAY_RETRY = 15

PERDA_MAXIMA = 0.15
MAX_LOSSES_SEGUIDOS = 2

MAX_TRADES_POR_DIA = 9
trades_count = 0
last_day = date.today()

def calcular_ema(closes, periodo):
    k = 2 / (periodo + 1)
    ema = closes[0]
    for price in closes[1:]:
        ema = price * k + ema * (1 - k)
    return ema

def calcular_atr(candles, periodo=14):
    trs = []
    for i in range(1, len(candles)):
        high, low, prev = float(candles[i][2]), float(candles[i][3]), float(candles[i-1][4])
        trs.append(max(high - low, abs(high - prev), abs(low - prev)))
    return sum(trs[-periodo:]) / periodo if trs else 0

def decide_trade(candles):
    sinais = [
        avaliar_media_movel(candles),
        avaliar_momentum(candles),
        avaliar_price_action(candles),
        avaliar_rsi(candles),
        avaliar_volume(candles)
    ]
    buys = sinais.count('Buy')
    sells = sinais.count('Sell')
    if buys >= 4 and sells == 0:
        return 'Buy', buys, sinais
    if sells >= 4 and buys == 0:
        return 'Sell', sells, sinais
    return 'Hold', 0, sinais

def obter_candles(par):
    return client.fetch_ohlcv(par, timeframe=INTERVALO, limit=30)

def get_wallet_balance():
    return float(client.fetch_balance()['total']['USDT'])

def obter_preco_atual(par):
    return float(client.fetch_ticker(par)['last'])

def definir_alavancagem(par):
    try:
        client.set_leverage(ALAVANCAGEM, par)
    except Exception:
        pass

def execute_trade(sinal, consenso, candles, par):
    global trades_count, last_day

    if date.today() != last_day:
        trades_count = 0
        last_day = date.today()

    if trades_count >= MAX_TRADES_POR_DIA:
        print("🔒 Limite diário de trades atingido")
        return

    closes = [float(c[4]) for c in candles]
    if len(closes) >= 15:
        ema7 = calcular_ema(closes[-7:], 7)
        ema15 = calcular_ema(closes[-15:], 15)
        if (sinal == 'Buy' and ema7 <= ema15) or (sinal == 'Sell' and ema7 >= ema15):
            print(f"{par} – 🔍 sem entrada (EMA fora da tendência)")
            return

    preco = obter_preco_atual(par)
    atr = calcular_atr(candles)
    volume = float(candles[-1][5])
    avg_vol = sum(float(c[5]) for c in candles) / len(candles)
    if atr < preco * 0.0015:
        print(f"{par} – 🔍 sem entrada (ATR fraco: {atr:.5f})")
        return
    if volume < avg_vol * 0.9:
        print(f"{par} – 🔍 sem entrada (volume fraco: {volume:.2f} < média {avg_vol:.2f})")
        return

    saldo = get_wallet_balance()
    if 'saldo_inicial' not in globals():
        globals()['saldo_inicial'] = saldo
        globals()['losses_seguidos'] = 0

    if saldo <= globals()['saldo_inicial'] * (1 - PERDA_MAXIMA):
        send_telegram_message("⚠️ Travão: perda >15% do saldo inicial. Pausa 1h.")
        time.sleep(3600)
        return
    if globals()['losses_seguidos'] >= MAX_LOSSES_SEGUIDOS:
        send_telegram_message("⚠️ Anti-falha: 2 perdas seguidas. Pausa 1h.")
        globals()['losses_seguidos'] = 0
        time.sleep(3600)
        return

    definir_alavancagem(par)
    qty = round(saldo * 0.98 * ALAVANCAGEM / preco, 3)
    if qty < 0.001:
        return

    tp_mult, sl_mult = (10.0, 5.0) if sinal == 'Buy' else (7.0, 3.5)
    tp = preco + tp_mult * atr if sinal == 'Buy' else preco - tp_mult * atr
    sl = preco - sl_mult * atr if sinal == 'Buy' else preco + sl_mult * atr
    side = 'buy' if sinal == 'Buy' else 'sell'
    msg = f"{'📈 LONG' if sinal=='Buy' else '📉 SHORT'} {par} | Consenso {consenso}/5 | TP:{tp:.2f} SL:{sl:.2f}"

    try:
        ordem = client.create_order(
            symbol=par, type='market', side=side, amount=qty,
            params={
                'stopLossPrice': round(sl, 2),
                'takeProfitPrice': round(tp, 2),
                'leverage': ALAVANCAGEM
            }
        )
        send_telegram_message(msg + "\n📦 Ordem executada com sucesso.")
        globals()['losses_seguidos'] = 0
    except Exception as e:
        send_telegram_message(f"❌ Erro ao enviar ordem:\n{e}")
        globals()['losses_seguidos'] += 1

    trades_count += 1

def esperar_proximo_candle():
    now = datetime.utcnow()
    delay = 300 - (now.minute % 5) * 60 - now.second
    time.sleep(delay)

if __name__ == '__main__':
    print("🚀 BOT x50 ATIVO — VERSÃO CORRIGIDA")
    while True:
        try:
            esperar_proximo_candle()
            for par in PARES:
                print(f"\n📊 Analisando {par}...")
                for _ in range(MAX_TENTATIVAS):
                    try:
                        candles = obter_candles(par)
                        sinal, consenso, sinais = decide_trade(candles)
                        print(f"{par}: sinal={sinal}, consenso={consenso}, sinais={sinais}")
                        if sinal != 'Hold':
                            execute_trade(sinal, consenso, candles, par)
                        break
                    except Exception as e:
                        print(f"Erro em {par}: {e}")
                        time.sleep(DELAY_RETRY)
        except Exception as e:
            send_telegram_message(f"⚠️ Erro geral do bot: {e}")
            time.sleep(DELAY_RETRY)