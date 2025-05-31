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

def fetch_candles(par, interval="1min", limit=20):  # ✅ reduzido para 20
    try:
        symbol = par.replace("/", "-").upper()  # Ex: BTC/USDT → BTC-USDT
        url = f"https://api.kucoin.com/api/v1/market/candles?type={interval}&symbol={symbol}"

        with httpx.Client(timeout=10.0) as client:
            response = client.get(url)

        if response.status_code != 200:
            print(f"[ERRO] KuCoin respondeu com status {response.status_code}")
            return []

        data = response.json()
        candles_raw = data.get("data", [])

        if not candles_raw or len(candles_raw) < limit:
            print(f"[ERRO] Lista de candles insuficiente na resposta da KuCoin.")
            return []

        candles = []
        for item in reversed(candles_raw[-limit:]):
            candles.append({
                "timestamp": int(time.mktime(time.strptime(item[0], "%Y-%m-%dT%H:%M:%S.%fZ"))) * 1000,
                "open": float(item[1]),
                "close": float(item[2]),
                "high": float(item[3]),
                "low": float(item[4]),
                "volume": float(item[5])
            })

        print(f"[DEBUG] Candles recebidos da KuCoin para {par}: {candles}")
        return candles

    except Exception as e:
        print(f"[ERRO] Falha ao buscar candles da KuCoin: {e}")
        return []