import httpx
import time
import hmac
import hashlib
import json
import random
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
        simbolo = par.split("/")[0].lower()
        vs_currency = par.split("/")[1].lower()

        url = f"https://api.coingecko.com/api/v3/coins/{simbolo}/market_chart"
        params = {
            "vs_currency": vs_currency,
            "days": "1",
            "interval": "minutely"
        }

        headers = {
            "User-Agent": random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15"
            ])
        }

        with httpx.Client(timeout=10.0, headers=headers) as client:
            response = client.get(url, params=params)

        if response.status_code == 429:
            print(f"[ERRO] CoinGecko: Too Many Requests (429) — limite atingido.")
            return []

        if response.status_code == 401:
            print(f"[ERRO] CoinGecko: Unauthorized (401) — verifica o User-Agent.")
            return []

        if response.status_code != 200:
            print(f"[ERRO] CoinGecko respondeu com status {response.status_code}")
            return []

        data = response.json()
        prices = data.get("prices", [])

        if len(prices) < limit:
            print(f"[ERRO] Lista de candles insuficiente. Recebidos: {len(prices)}")
            return []

        candles = []
        for item in prices[-limit:]:
            timestamp = int(item[0])
            price = float(item[1])
            candles.append({
                "timestamp": timestamp,
                "open": price,
                "high": price,
                "low": price,
                "close": price,
                "volume": 0.0
            })

        print(f"[DEBUG] Candles recebidos da CoinGecko para {par}: {candles}")
        return candles

    except Exception as e:
        print(f"[ERRO] Falha ao buscar candles da CoinGecko: {e}")
        return []