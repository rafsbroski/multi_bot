from config import STOP_LOSS_PERCENTUAL, CAPITAL_MINIMO, TELEGRAM_ATIVO
from telegram_alerts import notificar_telegram

def verificar_limites(cliente):
    try:
        if cliente is None:
            raise ValueError("Cliente não está definido (None)")

        capital = cliente.obter_saldo_total()
        if capital < CAPITAL_MINIMO:
            if TELEGRAM_ATIVO:
                notificar_telegram(f"❌ Capital disponível ({capital:.2f} USDT) abaixo do mínimo exigido.")
            return False
        return True
    except Exception as e:
        if TELEGRAM_ATIVO:
            notificar_telegram(f"❌ Erro ao verificar capital: {e}")
        return False

def aplicar_stop_loss(cliente, par):
    try:
        if cliente is None:
            raise ValueError("Cliente não está definido (None)")

        cliente.definir_stop_loss_percentual(par, STOP_LOSS_PERCENTUAL)
    except Exception as e:
        if TELEGRAM_ATIVO:
            notificar_telegram(f"⚠ Erro ao aplicar stop-loss em {par}: {e}")

def verificar_protecao(cliente):
    return verificar_limites(cliente)