import time
from datetime import datetime, date
from dotenv import load_dotenv
load_dotenv()
from config import API_KEY, API_SECRET
import ccxt
import os
import requests

def enviar_telegram(mensagem):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("Token ou Chat ID do Telegram não definidos.")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": mensagem}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Erro ao enviar mensagem para o Telegram:", e)

exchange = ccxt.mexc({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'enableRateLimit': True,
    'options': {'defaultType': 'future'}
})

symbol = 'BTC/USDT:USDT'
leverage = 50

# Define o tamanho da posição (ajuste conforme o capital disponível)
position_size = 0.05

def obter_tendencia():
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=200)
    closes = [x[4] for x in ohlcv]

    ma10 = sum(closes[-10:]) / 10
    ma50 = sum(closes[-50:]) / 50

    if ma10 > ma50:
        return "long"
    elif ma10 < ma50:
        return "short"
    else:
        return "neutro"

def abrir_ordem(tendencia):
    side = 'buy' if tendencia == 'long' else 'sell'
    params = {
        'positionSide': 'LONG' if tendencia == 'long' else 'SHORT',
        'leverage': leverage
    }
    try:
        ordem = exchange.create_market_order(symbol, side, position_size, params=params)
        mensagem = f"✅ Ordem aberta: {tendencia.upper()} no par {symbol} às {datetime.now().strftime('%H:%M:%S')}"
        print(mensagem)
        enviar_telegram(mensagem)
    except Exception as e:
        mensagem = f"❌ Erro ao abrir ordem: {str(e)}"
        print(mensagem)
        enviar_telegram(mensagem)

def main():
    print("Robô Sniper iniciado...")
    enviar_telegram("🤖 Robô Sniper iniciado com sucesso!")

    while True:
        try:
            tendencia = obter_tendencia()
            if tendencia != "neutro":
                abrir_ordem(tendencia)
            else:
                print("🔍 Nenhuma tendência clara. Aguardando...")
            time.sleep(60)
        except Exception as e:
            mensagem = f"⚠️ Erro inesperado: {str(e)}"
            print(mensagem)
            enviar_telegram(mensagem)
            time.sleep(60)

if __name__ == "__main__":
    main()