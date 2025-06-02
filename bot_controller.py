from especialistas import (
    especialista_candle,
    especialista_macd,
    especialista_rsi,
    especialista_moving_average,
    especialista_price_action
)

from trading import executar_ordem
from telegram_alerts import notificar_telegram as enviar_mensagem

CONSENSO_MINIMO = 4  # Número mínimo de especialistas que devem concordar

def obter_sinal_consenso(par):
    sinais = []

    try:
        sinais.append(especialista_candle(par))
    except Exception as e:
        print(f"[ERRO] especialista_candle: {e}")

    try:
        sinais.append(especialista_macd(par))
    except Exception as e:
        print(f"[ERRO] especialista_macd: {e}")

    try:
        sinais.append(especialista_rsi(par))
    except Exception as e:
        print(f"[ERRO] especialista_rsi: {e}")

    try:
        sinais.append(especialista_moving_average(par))
    except Exception as e:
        print(f"[ERRO] especialista_moving_average: {e}")

    try:
        sinais.append(especialista_price_action(par))
    except Exception as e:
        print(f"[ERRO] especialista_price_action: {e}")

    # Contagem de sinais
    if sinais.count("long") >= CONSENSO_MINIMO:
        return "long"
    elif sinais.count("short") >= CONSENSO_MINIMO:
        return "short"
    else:
        return None

def executar_ordem_com_consenso(par):
    direcao = obter_sinal_consenso(par)
    if direcao:
        mensagem = f"[CONSENSO] {par}: Entrada detectada ({direcao.upper()}) por {CONSENSO_MINIMO}+ especialistas."
        enviar_mensagem(mensagem)
        executar_ordem(par, direcao)
    else:
        print(f"[INFO] Sem consenso suficiente para {par}. Nenhuma ordem executada.")