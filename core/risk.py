from __future__ import annotations

ATR_MULT_SL: float = 1.0        # 止损 = 1×ATR
ATR_MULT_TP: float = 1.5        # 止盈 = 1.5×ATR
RISK_PCT:    float = 0.02       # 每笔风险资本占用 2%

def calc_position_size(price: float, atr: float, risk_usd: float) -> float:
    """
    依据 ATR 止损幅度计算合约张数（或现货数量）:
    position = risk / (ATR_MULT_SL * atr)
    """
    dollar_per_unit = ATR_MULT_SL * atr
    if dollar_per_unit == 0:
        return 0.0
    qty = risk_usd / dollar_per_unit
    return round(qty, 3)

def build_risk(price: float, atr: float, balance: float) -> dict:
    risk_usd = balance * RISK_PCT
    qty      = calc_position_size(price, atr, risk_usd)
    sl       = price - ATR_MULT_SL * atr
    tp       = price + ATR_MULT_TP * atr
    return dict(risk_usd=risk_usd, qty=qty, sl=sl, tp=tp)
