import time
import logging

from config import PAIRS, CHECK_INTERVAL
from especialistas.candlestick_bot import analisar_candle    as especialista_candle
from especialistas.media_movel_bot import analisar_media_movel as especialista_media_movel
from especialistas.macd_bot         import analisar_macd      as especialista_macd
from especialistas.rsi_bot          import avaliar_rsi        as especialista_rsi
from especialistas.price_action_bot import avaliar_price_action as especialista_price_action

from trading   import executar_ordem
from protecao  import verificar_limites
from telegram_alerts import enviar_mensagem

# Logger básico
logging.basicConfig(
    level    = logging.INFO,
    format   = "%(asctime)s %(levelname)s: %(message)s",
    datefmt  = "%Y-%m-%d %H:%M:%S"
)

# Lista de especialistas na ordem que quiseres
especialistas = [
    especialista_candle,
    especialista_media_movel,
    especialista_macd,
    especialista_rsi,
    especialista_price_action,
]

def analisar_sinal(candles):
    """
    Executa cada especialista sobre 'candles' e devolve:
      - "long"  se ≥4 retornarem "buy"
      - "short" se ≥4 retornarem "sell"
      - None     caso contrário
    """
    resultados = []
    for f in especialistas:
        try:
            r = f(candles)
        except Exception as e:
            logging.error(f"[ERRO] {f.__name__}: {e}")
            r = None
        if r in ("buy", "sell"):
            resultados.append(r)

    if resultados.count("buy")  >= 4:
        return "long"
    if resultados.count("sell") >= 4:
        return "short"
    return None

def main():
    while True:
        for par in PAIRS:
            # ─── Obter os candles (adequa esta parte à tua fonte real) ───
            try:
                from mexc_api import fetch_ohlcv
                candles = fetch_ohlcv(par, timeframe="5m", limit=30)
            except Exception as e:
                logging.error(f"Erro a obter candles para {par}: {e}")
                continue
            # ──────────────────────────────────────────────────────────────

            logging.info(f"[VERIFICAÇÃO] Analisando sinais para {par}…")
            consenso = analisar_sinal(candles)

            if consenso:
                logging.info(f"→ Consenso: {consenso.upper()} em {par}")
                if verificar_limites():
                    sucesso = executar_ordem(par, consenso)
                    if sucesso:
                        enviar_mensagem(f"✅ Ordem {consenso.upper()} em {par} executada")
                else:
                    enviar_mensagem(f"⚠️ Limites impediram ordem em {par}")
            else:
                logging.info(f"[INFO] Sem consenso para {par}.")
            # Pequena pausa entre pares
            time.sleep(1)

        # Espera CHECK_INTERVAL minutos antes do próximo ciclo completo
        time.sleep(CHECK_INTERVAL * 60)

if __name__ == "__main__":
    main()
