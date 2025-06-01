import httpx
import time
import hmac
import hashlib
import json
from config import MEXC_API_KEY, MEXC_SECRET_KEY

BASE_URL = "https://api.mexc.com"


def _timestamp():
    return int(time.time() * 1000)


def _assinatura(params, secret_key):
    query_string = '&'.join(f"{k}={v}" for k, v in sorted(params.items()))
    return hmac.new(secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()


def _headers():
    return {
        "Content-Type": "application/json",
        "ApiKey": MEXC_API_KEY
    }


def criar_cliente():
    class ClienteMEXC:
        def __init__(self, api_key, secret_key):
            self.api_key = api_key
            self.secret_key = secret_key

        def obter_saldo_total(self):
            try:
                endpoint = "/api/v3/account"
                timestamp = _timestamp()
                params = {
                    "timestamp": timestamp
                }
                assinatura = _assinatura(params, self.secret_key)
                url = f"{BASE_URL}{endpoint}?timestamp={timestamp}&signature={assinatura}"
                headers = _headers()
                response = httpx.get(url, headers=headers)

                if response.status_code == 200:
                    dados = response.json()
                    saldo_total = 0.0
                    for ativo in dados.get("balances", []):
                        saldo = float(ativo.get("free", 0))
                        saldo_total += saldo
                    return saldo_total
                else:
                    print(f"[MEXC] Erro ao obter saldo: {response.status_code} - {response.text}")
                    return 0.0

            except Exception as e:
                print(f"[MEXC] Erro inesperado ao obter saldo: {e}")
                return 0.0

    try:
        cliente = ClienteMEXC(MEXC_API_KEY, MEXC_SECRET_KEY)
        # Testa já o saldo para verificar se a autenticação funciona
        saldo = cliente.obter_saldo_total()
        if saldo >= 0:
            print(f"[MEXC] Cliente autenticado. Saldo total: {saldo} USDT")
            return cliente
        else:
            print("[MEXC] Cliente não autenticado.")
            return False
    except Exception as e:
        print(f"[MEXC] Falha ao criar cliente: {e}")
        return False