# telegram_alerts.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_ATIVO = os.getenv("TELEGRAM_ATIVO", "False") == "True"

def notificar_telegram(mensagem):
    if TELEGRAM_ATIVO and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem}
        try:
            response = requests.post(url, data=data)
            if not response.ok:
                print(f"[TELEGRAM] Erro: {response.text}")
        except Exception as e:
            print(f"[TELEGRAM] Falha ao enviar mensagem: {e}")
    else:
        print(f"[TELEGRAM DESATIVADO] {mensagem}")

# ALIAS usado nos imports
enviar_mensagem = notificar_telegram