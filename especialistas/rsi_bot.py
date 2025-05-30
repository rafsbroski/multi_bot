import pandas as pd
import logging

def analisar_sinal(candles):
    try:
        if not isinstance(candles, list) or len(candles) < 15:
            raise ValueError("Estrutura de candles inválida ou insuficiente.")

        df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["close"] = pd.to_numeric(df["close"], errors="coerce")

        delta = df["close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        rsi_ultimo = rsi.iloc[-1]

        if rsi_ultimo < 30:
            return "compra"
        elif rsi_ultimo > 70:
            return "venda"
        else:
            return None

    except Exception as e:
        logging.error(f"especialista_rsi: {e}")
        return None