import time
from config import PAIRS, CHECK_INTERVAL
from especialistas import rsi_bot, media_movel_bot, macd_bot, candlestick_bot, price_action_bot
from trading import executar_ordem
from protecao import verificar_protecao
from telegram_alerts import enviar_mensagem

especialistas = [
    especialista_rsi,
    especialista_media_movel,
    especialista_macd,
    especialista_volume,
    especialista_price_action,
]

def analisar_sinal(precos, par):
    sinais = []
    for especialista in especialistas:
        try:
            sinal = especialista(precos)
            sinais.append(sinal)
        except Exception as e:
            print(f"[ERRO] Especialista falhou ({especialista.__name__}) para o par {par}: {e}")
            sinais.append(None)

    sinais_validos = [s for s in sinais if s in ['long', 'short']]
    consenso = None
    if sinais_validos.count('long') >= 4:
        consenso = 'long'
    elif sinais_validos.count('short') >= 4:
        consenso = 'short'
    
    return consenso

def obter_preco_atual(par):
    from mexc_api import obter_preco_atual
    return obter_preco_atual(par)

def main():
    while True:
        for par in PAIRS:
            try:
                preco_atual = obter_preco_atual(par)
                print(f"\n[{par}] Preço atual: {preco_atual}")
                consenso = analisar_sinal(preco_atual, par)

                if consenso:
                    if verificar_protecao():
                        print(f"[{par}] Sinal: {consenso.upper()} (com consenso de especialistas)")
                        executar_ordem(par, consenso)
                        enviar_mensagem(f"✅ Entrada realizada em {par} ({consenso.upper()}) com consenso.")
                    else:
                        print(f"[{par}] Proteção ativada. Nenhuma entrada foi realizada.")
                        enviar_mensagem(f"⚠️ Proteção ativada. Entrada em {par} ({consenso.upper()}) cancelada.")
                else:
                    print(f"[{par}] Sem consenso suficiente para entrada.")
            except Exception as erro:
                print(f"[ERRO] no par {par}: {erro}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()