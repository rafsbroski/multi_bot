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
            "price": "",
            "vol": str(tamanho),
            "side": lado,
            "type": 1,
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
    pass  # Placeholder

def verificar_posicoes_ativas(cliente, par):
    try:
        return False
    except Exception:
        return True

def fetch_candles(par, interval="1m", limit=50):
    try:
        endpoint = "/api/v3/klines"
        url = f"{BASE_URL}{endpoint}"
        symbol = par.replace("/", "")

        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"[ERRO] MEXC respondeu com status {response.status_code}")
            return []

        try:
            data = response.json()
        except Exception as e:
            print(f"[ERRO] JSON inválido da MEXC: {e}")
            return []

        if not isinstance(data, list) or len(data) < 30:
            print(f"[ERRO] Lista de candles insuficiente. Recebidos: {len(data)}")
            return []

        candles = []
        for item in data:
            try:
                candles.append({
                    "timestamp": int(item[0]),
                    "open": float(item[1]),
                    "high": float(item[2]),
                    "low": float(item[3]),
                    "close": float(item[4]),
                    "volume": float(item[5])
                })
            except Exception as e:
                print(f"[ERRO] Conversão de candle falhou: {e}")
                continue

        print(f"[DEBUG] Candles recebidos para {symbol}: {candles}")
        return candles

    except Exception as e:
        print(f"[ERRO] Falha ao buscar candles da MEXC: {e}")
        return []