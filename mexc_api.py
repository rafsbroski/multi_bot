import httpx
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
        response = httpx.post(url, headers=_headers(), json=params)
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
        symbol = par.replace("/", "-").lower()  # ✅ Corrigido para o formato da Pionex
        url = f"https://api.pionex.com/api/v1/market/kline?symbol={symbol}&interval=1m&limit={limit}"

        with httpx.Client(timeout=10.0) as client:
            response = client.get(url)

        if response.status_code != 200:
            print(f"[ERRO] Pionex respondeu com status {response.status_code}")
            return []

        data = response.json()
        if "data" not in data or len(data["data"]) < limit:
            print(f"[ERRO] Lista de candles insuficiente ou ausente na resposta da Pionex.")
            return []

        candles = []
        for item in data["data"][-limit:]:
            candles.append({
                "timestamp": int(item[0]),
                "open": float(item[1]),
                "high": float(item[2]),
                "low": float(item[3]),
                "close": float(item[4]),
                "volume": float(item[5])
            })

        print(f"[DEBUG] Candles recebidos da Pionex para {par}: {candles}")
        return candles

    except Exception as e:
        print(f"[ERRO] Falha ao buscar candles da Pionex: {e}")
        return []