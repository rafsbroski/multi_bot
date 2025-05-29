import os
import time
import logging
import telebot
from config import client, symbol, leverage, quantity, stop_loss_percent
from dotenv import load_dotenv
from helpers.entry_conditions import should_open_long, should_open_short
from helpers.exit_conditions import should_close_long, should_close_short
from helpers.order_execution import execute_long_entry, execute_short_entry, close_position

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def send_telegram_message(message):
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        logging.info(f"Mensagem enviada: {message}")
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem para o Telegram: {e}")

def main_loop():
    send_telegram_message("🤖 Bot iniciado com sucesso!")

    position = None
    entry_price = None

    while True:
        try:
            mark_price_data = client.get_market_price(symbol=symbol)
            mark_price = float(mark_price_data["price"])
            logging.info(f"Preço atual do mercado: {mark_price}")

            if position is None:
                if should_open_long(mark_price):
                    execute_long_entry(client, symbol, quantity, leverage)
                    position = "long"
                    entry_price = mark_price
                    send_telegram_message(f"🔼 Entrada em LONG a {entry_price}")
                elif should_open_short(mark_price):
                    execute_short_entry(client, symbol, quantity, leverage)
                    position = "short"
                    entry_price = mark_price
                    send_telegram_message(f"🔽 Entrada em SHORT a {entry_price}")

            elif position == "long":
                if should_close_long(mark_price, entry_price, stop_loss_percent):
                    close_position(client, symbol)
                    send_telegram_message(f"📤 Saída do LONG a {mark_price}")
                    position = None
                    entry_price = None

            elif position == "short":
                if should_close_short(mark_price, entry_price, stop_loss_percent):
                    close_position(client, symbol)
                    send_telegram_message(f"📤 Saída do SHORT a {mark_price}")
                    position = None
                    entry_price = None

            time.sleep(3)

        except Exception as e:
            logging.error(f"Erro na execução: {e}")
            send_telegram_message(f"⚠️ Erro detectado: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main_loop()