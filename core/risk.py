# core/risk.py

from typing import Literal

ACCOUNT_SIZE_USD: float = 10_000
RISK_PCT_PER_TRADE: float = 0.002
RISK_USD: float = ACCOUNT_SIZE_USD * RISK_PCT_PER_TRADE

ATR_MULT_SL: float = 1.5
ATR_MULT_TP: float = 2.0

def calc_position_size(
    price: float,
    risk_usd: float,
    atr_mult_sl: float,
    atr_value: float,
    side: Literal["long", "short"],
) -> float:
    sl_distance = atr_mult_sl * atr_value
    if sl_distance <= 0:
        raise ValueError("ATR must be positive")
    qty = risk_usd / sl_distance
    return qty

__all__ = [
    "RISK_USD",
    "ATR_MULT_SL",
    "ATR_MULT_TP",
    "calc_position_size",
]
