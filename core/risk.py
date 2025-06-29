# core/risk.py

from typing import Literal

ACCOUNT_SIZE_USD = 10_000
RISK_PCT_PER_TRADE = 0.002
RISK_USD = ACCOUNT_SIZE_USD * RISK_PCT_PER_TRADE

ATR_MULT_SL = 1.5
ATR_MULT_TP = 2.0

def calc_position_size(
    price: float,
    risk_usd: float,
    atr_mult_sl: float,
    atr_value: float,
    side: Literal["long","short"],
) -> float:
    sl_distance = atr_mult_sl * atr_value
    if sl_distance <= 0:
        raise ValueError("ATR must be positive")
    return risk_usd / sl_distance
