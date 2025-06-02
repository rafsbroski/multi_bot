import time
import requests
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
    index = 0
    forcar_entrada = True  # 👈 Simulação de entrada
    sucesso, cliente = criar_cliente()

    if not sucesso or cliente is None:
        print("[ERRO] Cliente MEXC não pôde ser autenticado. Encerrando execução.")
        return

    # 👇 Teste direto de ligação à MEXC
    try:
        print("[TESTE] A testar ligação externa à API da MEXC...")
        resposta = requests.get("https://api.mexc.com/api/v1/time", timeout=10)
        if resposta.status_code == 200:
            print("[TESTE] Ligação externa à MEXC confirmada com sucesso.")
        else:
            print(f"[ERRO] Falha na ligação externa à MEXC. Código {resposta.status_code}")
            enviar_mensagem(f"❌ Falha na ligação externa à MEXC. Código {resposta.status_code}")
            return
    except Exception as e:
        print(f"[ERRO] Erro ao testar ligação externa à MEXC: {e}")
        enviar_mensagem(f"❌ Erro ao testar ligação externa à MEXC: {e}")
        return

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

        # 👇 BLOCO DE TESTE FORÇADO — executa 1 vez
        if forcar_entrada:
            print("[SIMULAÇÃO] A forçar uma entrada LONG em BTC/USDT...")
            if verificar_protecao(cliente):
                sucesso = executar_ordem("BTC/USDT", "long")
                if sucesso:
                    enviar_mensagem("🧪 Ordem de TESTE LONG em BTC/USDT executada.")
                else:
                    enviar_mensagem("❌ Falha ao executar ordem de teste.")
            else:
                print("[FORÇADO] Proteção ativa, ordem forçada cancelada.")
                enviar_mensagem("⚠️ Proteção ativa, ordem forçada cancelada.")
            forcar_entrada = False  # Não repete

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