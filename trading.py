# trading.py

from mexc_api import abrir_posicao, fechar_posicoes_anteriores, verificar_posicoes_ativas
from protecao import verificar_limites, aplicar_stop_loss
from telegram_alerts import enviar_mensagem
from config import PAIRS, RISCO_POR_TRADE

def executar_ordem(par: str, direcao: str):
    """
    Executa uma ordem de mercado em 'par' com direção 'long' ou 'short'.
    Primeiro verifica proteções, depois checa se já não existe
    posição ativa e enfim abre a ordem e aplica stop-loss.
    """
    # 1) Proteção geral (capital mínimo, drawdown, etc)
    if not verificar_limites():
        enviar_mensagem(f"🚨 Operação bloqueada por limites de segurança ({par})")
        return False

    # 2) Só abre se não houver posição ativa
    if verificar_posicoes_ativas(par):
        enviar_mensagem(f"⚠️ Já existe uma posição aberta em {par}")
        return False

    # 3) Fecha ordens anteriores (se houver)
    fechar_posicoes_anteriores(par)

    # 4) Calcula tamanho de acordo com risco por trade
    from mexc_api import client
    saldo = client.fetch_balance()['free']['USDT']
    tamanho = round(saldo * RISCO_POR_TRADE, 2)
    if tamanho <= 0:
        enviar_mensagem(f"❌ Saldo insuficiente para abrir posição em {par}")
        return False

    # 5) Abre a ordem
    sucesso = abrir_posicao(par, direcao, tamanho)
    if not sucesso:
        enviar_mensagem(f"❌ Falha ao abrir {direcao.upper()} em {par}")
        return False

    enviar_mensagem(f"✅ Entrada {direcao.upper()} em {par} de {tamanho} USDT")

    # 6) Configura stop-loss
    try:
        aplicar_stop_loss(par)
    except Exception as e:
        # só loga, mas não impede a ordem
        print(f"[WARN] falha ao aplicar stop-loss em {par}: {e}")

    return True