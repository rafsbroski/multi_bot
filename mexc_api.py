import requests
import time
import hmac
import hashlib
import json
from config import MEXC_API_KEY, MEXC_SECRET_KEY

BASE_URL = "https://api.mexc.com"

def _assinatura(params, secret_key):
    query_string = '&'.join(f"{k}={v}" for k, v in sorted(params.items()))
    return hmac.new(secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def _headers():
    return {
        "Content-Type": "application/json",
        "ApiKey": MEXC_API_KEY
    }

def _timestamp():
    return int(time.time() * 1000)

def abrir_posicao(cliente, par, direcao, tamanho):
    try:
        endpoint = "/api/v1/order"
        url = BASE_URL + endpoint

        lado = "BUY" if direcao == "long" else "SELL"

        params = {
            "symbol": par.replace("/", "_"),
            "price": "",  # Preço de mercado
            "vol": str(tamanho),
            "side": lado,
            "type": 1,  # Ordem a mercado
            "open_type": "isolated",
            "position_id": 0,
            "leverage": 50,
            "external_oid": str(_timestamp()),
            "stop_loss_price": "",
            "take_profit_price": "",
            "position_mode": "hedge_mode",
            "timestamp": _timestamp()
        }

        params["sign"] = _assinatura(params, MEXC_SECRET_KEY)
        response = requests.post(url, headers=_headers(), json=params)
        return response.status_code == 200
    except Exception as e:
        print(f"Erro ao abrir posição: {e}")
        return False

def fechar_posicoes_anteriores(cliente, par):
    # Esta função pode ser desenvolvida no futuro se quisermos encerrar posições manualmente
    pass

def verificar_posicoes_ativas(cliente, par):
    try:
        # Aqui poderia-se ligar ao endpoint de posições
        return False  # Supondo que ainda não temos nada aberto
    except Exception:
        return True  # Por segurança, assumimos que há