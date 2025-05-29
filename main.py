from candlestick_bot import analisar_sinal as candle_sinal
from macd_bot import analisar_sinal as macd_sinal
from rsi_bot import analisar_sinal as rsi_sinal
from tendencia_bot import analisar_sinal as tendencia_sinal
from volume_bot import analisar_sinal as volume_sinal
from telegram_alerts import notificar_telegram as enviar_mensagem
from bot_controller import executar_ordem

import time

pares = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]

def analisar_par(par):
    sinais = [
        candle_sinal(par),
        macd_sinal(par),
        rsi_sinal(par),
        tendencia_sinal(par),
        volume_sinal(par)
    ]
    sinais_positivos = sinais.count("long")
    sinais_negativos = sinais.count("short")

    if sinais_positivos >= 4:
        enviar_mensagem(f"[{par}] CONSENSO POSITIVO - LONG ({sinais_positivos}/5)")
        executar_ordem(par, "long")
    elif sinais_negativos >= 4:
        enviar_mensagem(f"[{par}] CONSENSO NEGATIVO - SHORT ({sinais_negativos}/5)")
        executar_ordem(par, "short")
    else:
        enviar_mensagem(f"[{par}] SEM CONSENSO - Nenhuma entrada")

if __name__ == "__main__":
    while True:
        for par in pares:
            try:
                analisar_par(par)
            except Exception as e:
                enviar_mensagem(f"[{par}] ERRO: {str(e)}")
        time.sleep(900)  # Espera 15 minutos antes da próxima análise