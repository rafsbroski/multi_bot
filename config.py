import os
from dotenv import load_dotenv

load_dotenv()

# Chaves da MEXC (vindas do ficheiro .env)
MEXC_API_KEY = os.getenv("API_KEY")
MEXC_SECRET_KEY = os.getenv("API_SECRET")

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Lista de pares a operar (todos USDT-M)
PAIRS = ["BTC/USDT", "ETH/USDT", "SOL/USDT"]

# Intervalo de análise dos candles (em minutos)
CHECK_INTERVAL = 1

# Alavancagem fixa (x50)
ALAVANCAGEM = 50

# Risco máximo por operação (% do saldo)
RISCO_POR_TRADE = 0.05  # 5%

# Proteção inteligente
STOP_LOSS_PERCENTUAL = 5     # Stop-loss por trade (%)
CAPITAL_MINIMO = 5           # Capital mínimo para abrir trade (USDT)
RETIRADA_SEMANAL = 0.10      # Retirada semanal de 10% dos lucros
TELEGRAM_ATIVO = True        # True para receber alertas

# Consenso dos especialistas
MINIMO_CONSENSO = 4  # de 5

# Limite de trades por dia (0 = ilimitado)
MAX_TRADES_DIA = 0