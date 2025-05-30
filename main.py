# src/main.py

import time
import logging

from config import PAIRS, CHECK_INTERVAL
from bot_controller import executar_ordem

from especialistas.candlestick_bot      import analisar_candle      as especialista_candle
from especialistas.macd_bot             import analisar_macd        as especialista_macd
from especialistas.rsi_bot              import avaliar_rsi          as especialista_rsi
from especialistas.media_movel_bot      import avaliar_media_movel  as especialista_media_movel
from especialistas.price_action_bot     import avaliar_price_action as especialista_price_action

ESPECIALISTAS = [
    especialista_candle,
    especialista_macd,
    especialista_rsi,
    especialista_media_movel,
    especialista_price_action,
]

def analisar_consenso(candles, par):
    sinais = []
    for esp in ESPECIALISTAS:
        try:
            sinais.append(esp(candles))
        except Exception as e:
            logging.error(f"[ERRO] {esp.__name__}: {e}")
    longs  = sinais.count("long")
    shorts = sinais.count("short")
    if longs >= 4:
        return "long"
    if shorts >= 4:
        return "short"
    return None

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")
    while True:
        for par in PAIRS:
            try:
                from mexc_api import obter_candles
                candles = obter_candles(par)

                logging.info(f"[VERIFICAÇÃO] {par} → obtendo sinal...")
                direcao = analisar_consenso(candles, par)

                if direcao:
                    logging.info(f"[INFO] Consenso {direcao.upper()} em {par}")
                    executar_ordem(par, direcao)
                else:
                    logging.info(f"[INFO] Sem consenso em {par}.")
            except Exception as e:
                logging.error(f"[ERRO] loop principal ({par}): {e}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()