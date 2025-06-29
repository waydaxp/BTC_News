# core/risk.py
"""
与仓位、止损 / 止盈相关的统一计算逻辑
------------------------------------------------
其他模块只 import 常量 + calc_position_size 即可。
"""

from typing import Literal


# === 全局风控参数（集中修改） =============================================== #
ACCOUNT_SIZE_USD: float = 10_000          # ∙ 账户总权益（方便统一调整）
RISK_PCT_PER_TRADE: float = 0.002         # ∙ 单笔风险占比 0.2% ⇒ 0.002
RISK_USD: float = ACCOUNT_SIZE_USD * RISK_PCT_PER_TRADE

ATR_MULT_SL: float = 1.5                  # ∙ 止损 = ± 1.5 ATR
ATR_MULT_TP: float = 2.0                  # ∙ 止盈 = ± 2.0 ATR  (≈1:R=1.33)

# 你也可以写到 config.yaml，再用 yaml.safe_load 读进来；此处为最简方式。


# === 仓位计算 ================================================================ #
def calc_position_size(
    price: float,
    risk_usd: float,
    atr_mult_sl: float,
    atr_value: float,
    side: Literal["long", "short"],
) -> float:
    """
    根据 ATR 止损距离 → 反推可承受风险 USD → 计算合约张数（等同名义价值）
    公式：
        sl_distance = atr_mult_sl * atr_value
        qty = risk_usd / sl_distance
    side 不影响结果，保持参数一致以便调用方传递。
    """
    sl_distance = atr_mult_sl * atr_value
    if sl_distance <= 0:
        raise ValueError("ATR must be positive")

    qty = risk_usd / sl_distance
    return qty


# === 方便外部引用 __all__ ==================================================== #
__all__ = [
    "RISK_USD",
    "ATR_MULT_SL",
    "ATR_MULT_TP",
    "calc_position_size",
]
