from especialistas.candlestick_bot import analisar_sinal as especialista_candle
from especialistas.macd_bot import analisar_sinal as especialista_macd
from especialistas.rsi_bot import analisar_sinal as especialista_rsi
from especialistas.media_movel_bot import analisar_sinal as especialista_moving_average
from especialistas.price_action_bot import analisar_sinal as especialista_price_action

from telegram_alerts import notificar_telegram as enviar_mensagem
from bot_controller import executar_ordem_com_consenso
from config import PAIRS, CHECK_INTERVAL

import time

def main():
    while True:
        for par in PAIRS:
            print(f"\n[VERIFICAÇÃO] Analisando sinal para {par}...")
            try:
                executar_ordem_com_consenso(par)
            except Exception as e:
                print(f"[ERRO] ao executar ordem com consenso para {par}: {e}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
