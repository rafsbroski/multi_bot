import random
from mexc_api import abrir_posicao, fechar_posicoes_anteriores, verificar_posicoes_ativas
from protecao import verificar_limites, aplicar_stop_loss
from telegram_alerts import notificar_telegram
from config import PAIRS

def executar_ordem(sinais_especialistas, cliente):
    for par in PAIRS:
        sinais = sinais_especialistas.get(par, [])
        if len(sinais) == 0:
            continue

        direcao_final = analisar_consenso(sinais)

        if direcao_final is None:
            continue

        if not verificar_limites(cliente):
            notificar_telegram(f"🚨 Operação bloqueada por limites de segurança ({par})")
            continue

        if verificar_posicoes_ativas(cliente, par):
            notificar_telegram(f"⚠ Já existe uma posição aberta em {par}")
            continue

        fechar_posicoes_anteriores(cliente, par)

        tamanho = calcular_tamanho_posicao(cliente, par)
        if tamanho <= 0:
            notificar_telegram(f"❌ Tamanho da posição em {par} é inválido.")
            continue

        resultado = abrir_posicao(cliente, par, direcao_final, tamanho)

        if resultado:
            notificar_telegram(f"✅ Entrada {direcao_final.upper()} em {par} com {tamanho} USDT.")
        else:
            notificar_telegram(f"❌ Falha ao abrir posição em {par}.")

        aplicar_stop_loss(cliente, par)

def analisar_consenso(sinais):
    if len(sinais) < 5:
        return None
    long_count = sinais.count("long")
    short_count = sinais.count("short")
    if long_count >= 4:
        return "long"
    elif short_count >= 4:
        return "short"
    else:
        return None

def calcular_tamanho_posicao(cliente, par):
    try:
        saldo = cliente.obter_saldo_disponivel()
        tamanho = saldo * 0.95  # usa 95% do capital disponível
        return round(tamanho, 2)
    except Exception as e:
        print(f"Erro ao calcular tamanho: {e}")
        return 0