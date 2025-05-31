import httpx
import time
import hmac
import hashlib
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
    pass  # ainda por implementar

def verificar_posicoes_ativas(cliente, par):
    try:
        return False
    except Exception:
        return True

def fetch_candles(par, interval="1min", limit=20):
    symbol_kucoin = par.replace("/", "-").upper()
    symbol_binance = par.replace("/", "").lower()
    symbol_coingecko = par.replace("/", "").lower()

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        url = f"https://api.kucoin.com/api/v1/market/candles?type={interval}&symbol={symbol_kucoin}"
        response = httpx.get(url, timeout=10)
        data = response.json().get("data", [])
        if data and len(data) >= limit:
            candles = []
            for item in reversed(data[-limit:]):
                candles.append({
                    "timestamp": int(time.mktime(time.strptime(item[0], "%Y-%m-%dT%H:%M:%S.%fZ"))) * 1000,
                    "open": float(item[1]),
                    "close": float(item[2]),
                    "high": float(item[3]),
                    "low": float(item[4]),
                    "volume": float(item[5])
                })
            print(f"[KUCOIN] Candles para {par}: OK")
            return candles
    except Exception as e:
        print(f"[KUCOIN] Erro: {e}")

    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol_binance.upper()}&interval=1m&limit={limit}"
        response = httpx.get(url, timeout=10)
        data = response.json()
        if isinstance(data, list) and len(data) >= limit:
            candles = []
            for item in data:
                candles.append({
                    "timestamp": int(item[0]),
                    "open": float(item[1]),
                    "high": float(item[2]),
                    "low": float(item[3]),
                    "close": float(item[4]),
                    "volume": float(item[5])
                })
            print(f"[BINANCE] Candles para {par}: OK")
            return candles
    except Exception as e:
        print(f"[BINANCE] Erro: {e}")

    try:
        url = f"https://api.coingecko.com/api/v3/coins/{symbol_coingecko}/market_chart?vs_currency=usd&days=1&interval=minutely"
        response = httpx.get(url, headers=headers, timeout=10)
        data = response.json().get("prices", [])
        if data and len(data) >= limit:
            candles = []
            for item in data[-limit:]:
                candles.append({
                    "timestamp": int(item[0]),
                    "open": float(item[1]),
                    "close": float(item[1]),
                    "high": float(item[1]),
                    "low": float(item[1]),
                    "volume": 0.0
                })
            print(f"[COINGECKO] Candles para {par}: OK")
            return candles
    except Exception as e:
        print(f"[COINGECKO] Erro: {e}")

    print(f"[ERRO] Nenhuma API devolveu candles para {par}.")
    return []