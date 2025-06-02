import httpx
import time
import hmac
import hashlib
from config import MEXC_API_KEY, MEXC_SECRET_KEY

BASE_URL = "https://contract.mexc.com"

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

def criar_cliente():
    try:
        url = f"{BASE_URL}/api/v1/private/account/assets"
        timestamp = _timestamp()
        params = {
            "timestamp": timestamp
        }
        assinatura = _assinatura(params, MEXC_SECRET_KEY)
        params["sign"] = assinatura

        cliente = httpx.Client(timeout=httpx.Timeout(10.0))
        response = cliente.post(url, headers=_headers(), json=params)

        if response.status_code == 200 and "data" in response.json():
            print("[MEXC] Cliente autenticado com as chaves configuradas.")
            return True, cliente
        else:
            print(f"[MEXC] Falha na autenticação. Código: {response.status_code} - Resposta: {response.text}")
            return False, None
    except Exception as e:
        print(f"[MEXC] Erro ao autenticar cliente: {e}")
        return False, None