from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_ATIVO
import requests

def notificar_telegram(mensagem):
    if TELEGRAM_ATIVO and TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem}
        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar mensagem para o Telegram: {e}")