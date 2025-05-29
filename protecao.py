from config import STOP_LOSS_PERCENTUAL, CAPITAL_MINIMO, TELEGRAM_ATIVO
from telegram_alerts import notificar_telegram

# Simulação de função para verificar capital mínimo
def verificar_limites(cliente):
    try:
        saldo = cliente.obter_saldo_disponivel()
        if saldo < CAPITAL_MINIMO:
            if TELEGRAM_ATIVO:
                notificar_telegram(f"❌ Capital disponível insuficiente: {saldo} USDT")
            return False
        return True
    except Exception as e:
        print(f"Erro ao verificar limites: {e}")
        return False

# Simulação de aplicação de stop-loss (no futuro poderá usar ordens reais)
def aplicar_stop_loss(cliente, par):
    try:
        # Esta função é onde se configuraria o stop-loss real na exchange, por enquanto é apenas lógica simulada
        print(f"Stop-loss de {STOP_LOSS_PERCENTUAL}% configurado para {par}")
    except Exception as e:
        print(f"Erro ao aplicar stop-loss: {e}")