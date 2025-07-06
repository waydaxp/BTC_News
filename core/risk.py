from typing import Literal

# 总账户资金
ACCOUNT_SIZE_USD: float = 10_000

# 风格模式：conservative, balanced, aggressive
DEFAULT_MODE: Literal["conservative", "balanced", "aggressive"] = "balanced"

# 风格配置参数
MODE_CONFIG = {
    "conservative": {
        "risk_pct": 0.001,
        "atr_sl": 1.2,
        "atr_tp": 1.8,
    },
    "balanced": {
        "risk_pct": 0.002,
        "atr_sl": 1.5,
        "atr_tp": 2.0,
    },
    "aggressive": {
        "risk_pct": 0.004,
        "atr_sl": 1.8,
        "atr_tp": 2.5,
    },
}

def get_risk_params(mode: Literal["conservative", "balanced", "aggressive"] = DEFAULT_MODE):
    cfg = MODE_CONFIG.get(mode, MODE_CONFIG["balanced"])
    risk_usd = ACCOUNT_SIZE_USD * cfg["risk_pct"]
    return cfg["atr_sl"], cfg["atr_tp"], risk_usd

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
    "DEFAULT_MODE",
    "get_risk_params",
    "calc_position_size",
]
