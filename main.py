import time
import logging

from config import PAIRS, CHECK_INTERVAL

# Importa cada especialista pelo nome real da função que definiste
from especialistas.candlestick_bot     import analisar_candle       as especialista_candle
from especialistas.media_movel_bot     import avaliar_media_movel   as especialista_media_movel
from especialistas.macd_bot            import analisar_macd         as especialista_macd
from especialistas.rsi_bot             import avaliar_rsi           as especialista_rsi
from especialistas.price_action_bot    import avaliar_price_action  as especialista_price_action

from trading          import executar_ordem
from protecao         import verificar_limites
from telegram_alerts  import enviar_mensagem

# Logger básico
logging.basicConfig(
    level   = logging.INFO,
    format  = "%(asctime)s %(levelname)s: %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S"
)

especialistas = [
    especialista_candle,
    especialista_media_movel,
    especialista_macd,
    especialista_rsi,
    especialista_price_action,
]

def analisar_sinal(candles):
    """
    Chama cada especialista; conta 'buy' vs 'sell'.
    Retorna 'long' se ≥4 'buy', 'short' se ≥4 'sell', senao None.
    """
    votos = []
    for f in especialistas:
        try:
            r = f(candles)
        except Exception as e:
            logging.error(f"[ERRO] {f.__name__}: {e}")
            r = None
        # uniformiza maiúsculas/minúsculas
        if isinstance(r, str) and r.lower() in ("buy", "compra"):
            votos.append("buy")
        elif isinstance(r, str) and r.lower() in ("sell", "venda"):
            votos.append("sell")

    if votos.count("buy")  >= 4:
        return "long"
    if votos.count("sell") >= 4:
        return "short"
    return None

def main():
    while True:
        for par in PAIRS:
            # ─── Obtém os candles (ajusta à tua função real) ───
            try:
                from mexc_api import fetch_ohlcv
                candles = fetch_ohlcv(par, timeframe="5m", limit=30)
            except Exception as e:
                logging.error(f"Erro a obter candles [{par}]: {e}")
                continue

            logging.info(f"[VERIFICAÇÃO] {par}")
            consenso = analisar_sinal(candles)

            if consenso:
                logging.info(f"→ Consenso: {consenso.upper()} em {par}")
                if verificar_limites():
                    if executar_ordem(par, consenso):
                        enviar_mensagem(f"✅ Ordem {consenso.upper()} em {par} executada")
                else:
                    enviar_mensagem(f"⚠️ Ordem em {par} bloqueada por limites")
            else:
                logging.info(f"[INFO] Sem consenso para {par}")

            time.sleep(1)  # pausa curta entre pares

        time.sleep(CHECK_INTERVAL * 60)

if __name__ == "__main__":
    main()