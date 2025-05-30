# especialistas/rsi_bot.py
import logging

def analisar_sinal(candles):
    """
    RSI curto (10) sobre closes dos últimos candles:
    retorna 'long' se RSI < 36, 'short' se RSI > 64, ou False.
    """
    try:
        # valida entrada
        if not isinstance(candles, list) or len(candles) < 11:
            raise ValueError("Estrutura de candles inválida ou insuficiente.")
        # extrai closes
        closes = []
        for c in candles:
            if isinstance(c, dict) and "close" in c:
                closes.append(float(c["close"]))
            elif isinstance(c, (list, tuple)) and len(c) > 4:
                closes.append(float(c[4]))
            else:
                raise ValueError("Formato de candle inválido.")
        # calcula RSI de período 10
        periodo = 10
        ganhos = perdas = 0.0
        for i in range(-periodo, 0):
            delta = closes[i] - closes[i-1]
            if delta > 0:
                ganhos += delta
            else:
                perdas -= delta
        if perdas == 0:
            rsi = 100.0
        else:
            rs = ganhos / perdas
            rsi = 100 - (100 / (1 + rs))
        # sinal
        if rsi < 36:
            return "long"
        if rsi > 64:
            return "short"
        return False
    except Exception as e:
        logging.error(f"[especialista_rsi] {e}")
        return False
