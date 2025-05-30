import pandas as pd
import logging

def analisar_sinal(candles):
    try:
        if not isinstance(candles, list) or len(candles) < 5:
            raise ValueError("Estrutura de candles inválida ou insuficiente.")

        df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["close"] = pd.to_numeric(df["close"], errors="coerce")

        candle_atual = df.iloc[-1]
        candle_anterior = df.iloc[-2]

        if (
            candle_atual["close"] > candle_atual["open"] and
            candle_anterior["close"] < candle_anterior["open"]
        ):
            return "compra"

        elif (
            candle_atual["close"] < candle_atual["open"] and
            candle_anterior["close"] > candle_anterior["open"]
        ):
            return "venda"

        return None

    except Exception as e:
        logging.error(f"especialista_price_action: {e}")
        return None