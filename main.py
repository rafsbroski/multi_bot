import time
from config import PAIRS, CHECK_INTERVAL
from especialistas.media_movel_bot   import avaliar_media_movel   as media_movel_sinal
from especialistas.rsi_bot           import avaliar_rsi          as rsi_sinal
from especialistas.price_action_bot  import avaliar_price_action as price_action_sinal
from especialistas.candlestick_bot   import analisar_candle      as candlestick_sinal
from especialistas.macd_bot          import analisar_macd        as macd_sinal
from protecao                        import verificar_protecao
from mexc_api                        import obter_preco_atual
from trading                         import executar_trading
from telegram_alerts                 import send_telegram_message

def main():
    while True:
        for par in PAIRS:
            try:
                # obtém lista de candles 1m (implemente fetch_ohlcv em mexc_api)
                candles = obter_preco_atual(par)  
                # aplica cada especialista
                sinais = [
                    media_movel_sinal(candles),
                    rsi_sinal(candles),
                    price_action_sinal(candles),
                    candlestick_sinal(candles),
                    macd_sinal(candles),
                ]
                # filtra apenas sinais válidos
                votos = [s for s in sinais if s in ("Buy","Sell","compra","venda")]
                # normaliza para "long"/"short"
                votos = [
                    "long" if s in ("Buy","compra") else "short"
                    for s in votos
                ]
                consenso = None
                if votos.count("long")  >= 4:
                    consenso = "long"
                elif votos.count("short") >= 4:
                    consenso = "short"

                if consenso:
                    if verificar_protecao():
                        executar_trading(par, consenso)
                        send_telegram_message(f"✅ Entrada {consenso.upper()} em {par}")
                    else:
                        send_telegram_message(f"⚠️ Proteção ativada em {par}, ordem cancelada.")
                else:
                    print(f"[{par}] Sem consenso suficiente ({sinais})")

            except Exception as e:
                print(f"[ERRO] {par}: {e}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()