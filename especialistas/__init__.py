# src/especialistas/__init__.py

# Cada especialista exporta a função que de fato existe no seu módulo:
from .candlestick_bot   import analisar_candle      as especialista_candle
from .macd_bot          import analisar_macd        as especialista_macd
from .rsi_bot           import avaliar_rsi           as especialista_rsi
from .media_movel_bot   import avaliar_media_movel  as especialista_moving_average
from .price_action_bot  import avaliar_price_action as especialista_price_action

__all__ = [
    "especialista_candle",
    "especialista_macd",
    "especialista_rsi",
    "especialista_moving_average",
    "especialista_price_action",
]
