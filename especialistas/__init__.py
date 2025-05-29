# especialistas/__init__.py

from .media_movel_bot import avaliar_media_movel as especialista_moving_average
from .price_action_bot import analisar_sinal    as especialista_price_action
from .rsi_bot        import avaliar_rsi         as especialista_rsi
from .candlestick_bot import analisar_candle    as especialista_candlestick
from .macd_bot       import analisar_macd       as especialista_macd

