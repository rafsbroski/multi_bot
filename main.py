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
from mexc_api import fetch_candles, criar_cliente

def main():
    cliente = criar_cliente()
    index = 0
    entrada_forcada = True  # Apenas para a primeira execução

    while True:
        par = PAIRS[index % len(PAIRS)]
        index += 1

        print(f"\n[VERIFICAÇÃO] Analisando sinal para {par}…")
        candles = fetch_candles(par, interval=CHECK_INTERVAL)

        print(f"[DEBUG] Candles recebidos no main para {par}: {candles}")

        if not candles or len(candles) < 20:
            print(f"[ERRO] Lista de candles vazia ou insuficiente para {par}.")
            time.sleep(CHECK_INTERVAL)
            continue

        # 🔥 Simulação de entrada forçada apenas 1 vez
        if entrada_forcada and par == "BTC/USDT":
            entrada_forcada = False
            if verificar_protecao(cliente):
                print(f"[FORÇADO] Ordem LONG forçada em {par}.")
                sucesso = executar_ordem(par, "long")
                if sucesso:
                    enviar_mensagem(f"✅ Ordem LONG forçada executada em {par}.")
            else:
                print(f"[FORÇADO] Proteção ativa, ordem forçada cancelada.")
                enviar_mensagem(f"⚠️ Proteção ativa, ordem forçada cancelada.")
            time.sleep(CHECK_INTERVAL)
            continue

        sinais = []
        for bot_fn in [
            especialista_candle,
            especialista_macd,
            especialista_rsi,
            especialista_media_movel,
            especialista_price_action
        ]:
            try:
                sinal = bot_fn(candles, par)
            except Exception as e:
                print(f"[ERRO] {bot_fn.__name__}: {e}")
                sinal = None
            sinais.append(sinal)

        longs = sum(1 for s in sinais if str(s).lower() in ("long", "buy", "compra"))
        shorts = sum(1 for s in sinais if str(s).lower() in ("short", "sell", "venda"))

        if longs >= 4 and shorts == 0:
            direcao = "long"
        elif shorts >= 4 and longs == 0:
            direcao = "short"
        else:
            print(f"[INFO] Sem consenso suficiente para {par}. Nenhuma ordem executada.")
            time.sleep(CHECK_INTERVAL)
            continue

        if verificar_protecao(cliente):
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