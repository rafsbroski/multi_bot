import time
from config import PAIRS, CHECK_INTERVAL
from especialistas import (
    especialista_candle,
    especialista_macd,
    especialista_rsi,
    especialista_media_movel,
    especialista_price_action,
)
from trading import executar_ordem
from protecao import verificar_protecao
from telegram_alerts import enviar_mensagem

def main():
    while True:
        for par in PAIRS:
            print(f"\n[VERIFICAÇÃO] Analisando sinal para {par}…")
            # Supondo que você tenha uma função que pega candles:
            from mexc_api import fetch_candles
            candles = fetch_candles(par, interval=CHECK_INTERVAL)
            # Para cada especialista, proteja contra estruturas inválidas:
            sinais = []
            for bot_fn in [
                especialista_candle,
                especialista_macd,
                especialista_rsi,
                especialista_moving_average,
                especialista_price_action
            ]:
                try:
                    sinal = bot_fn(candles, par)
                except Exception as e:
                    print(f"[ERRO] {bot_fn.__name__}: {e}")
                    sinal = None
                sinais.append(sinal)

            # Conta apenas 'long'/'buy' e 'short'/'sell'
            longs  = sum(1 for s in sinais if str(s).lower() in ("long", "buy", "compra"))
            shorts = sum(1 for s in sinais if str(s).lower() in ("short", "sell", "venda"))
            if longs >= 4 and shorts == 0:
                direcao = "long"
            elif shorts >= 4 and longs == 0:
                direcao = "short"
            else:
                print(f"[INFO] Sem consenso suficiente para {par}. Nenhuma ordem executada.")
                continue

            # Checa proteção e executa ordem
            if verificar_protecao():
                print(f"[INFO] Consenso para {par}: {direcao.upper()}. Tentando abrir posição…")
                sucesso = executar_ordem(par, direcao)
                if sucesso:
                    enviar_mensagem(f"✅ Ordem {direcao.upper()} executada em {par}.")
            else:
                print(f"[INFO] Proteção ativada. Entrada em {par} cancelada.")
                enviar_mensagem(f"⚠️ Proteção ativada. Entrada em {par} cancelada.")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()