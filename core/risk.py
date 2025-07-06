# core/risk.py

from typing import Literal

# 总账户资金
ACCOUNT_SIZE_USD: float = 10_000

# 默认交易风格模型：保守 / 均衡 / 攻击
DEFAULT_MODE: Literal["conservative", "balanced", "aggressive"] = "balanced"

# 各种风格的相关参数配置
MODE_CONFIG = {
    "conservative": {
        "risk_pct": 0.001,     # 每次交易风险 0.1%
        "atr_sl": 1.2,          # 止损 ATR 倍数
        "atr_tp": 1.8,          # 止益 ATR 倍数
    },
    "balanced": {
        "risk_pct": 0.002,     # 每次交易风险 0.2%
        "atr_sl": 1.5,
        "atr_tp": 2.0,
    },
    "aggressive": {
        "risk_pct": 0.004,     # 每次交易风险 0.4%
        "atr_sl": 1.8,
        "atr_tp": 2.5,
    },
}

# 根据风格返回相应的 ATR 止损/止益倍数和交易风险金额

def get_risk_params(mode: Literal["conservative", "balanced", "aggressive"] = DEFAULT_MODE):
    cfg = MODE_CONFIG.get(mode, MODE_CONFIG[DEFAULT_MODE])
    risk_usd = ACCOUNT_SIZE_USD * cfg["risk_pct"]
    return cfg["atr_sl"], cfg["atr_tp"], risk_usd

# 根据 ATR 计算付付付倍数和相应付金量

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
