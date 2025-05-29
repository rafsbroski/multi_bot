import time
from especialistas import (
    especialista_moving_average,
    especialista_volume,
    especialista_rsi,
    especialista_macd,
    especialista_price_action
)
from trading import executar_ordem
from telegram_alerts import enviar_alerta_telegram

PARES = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]
INTERVALO_ENTRE_ANALISES = 180  # segundos (3 minutos)
CONSENSO_MINIMO = 4

def obter_sinais(par):
    sinais = [
        especialista_moving_average.analisar(par),
        especialista_volume.analisar(par),
        especialista_rsi.analisar(par),
        especialista_macd.analisar(par),
        especialista_price_action.analisar(par)
    ]
    return sinais

def analisar_consenso(sinais):
    direcoes = [sinal for sinal in sinais if sinal in ["buy", "sell"]]
    if not direcoes:
        return None

    direcao_mais_comum = max(set(direcoes), key=direcoes.count)
    if direcoes.count(direcao_mais_comum) >= CONSENSO_MINIMO:
        return direcao_mais_comum
    return None

def iniciar_bot():
    while True:
        for par in PARES:
            sinais = obter_sinais(par)
            direcao = analisar_consenso(sinais)

            if direcao:
                mensagem = f"🧠 Consenso de {CONSENSO_MINIMO}+ especialistas: {direcao.upper()} em {par}"
                enviar_alerta_telegram(mensagem)
                executar_ordem(par, direcao)
            else:
                print(f"[{par}] Sem consenso suficiente. Nenhuma ordem executada.")

        time.sleep(INTERVALO_ENTRE_ANALISES)
