# core/risk.py
"""
统一风控 & 仓位计算模块
-------------------------------------------------
如需参数化（账户余额 / 杠杆 / ATR 倍数等），
后续可改为读取 config.yaml；现在先写死，保证脚本可跑通。
"""

ACCOUNT_USD   = 1_000          # 账户本金
RISK_PCT      = 0.02           # 每笔风险 2%
LEVERAGE      = 20             # 杠杆倍数
ATR_MULT_SL   = 1.0            # 止损 = entry ± 1 × ATR
ATR_MULT_TP   = 1.5            # 止盈 = entry ± 1.5 × ATR

# ---------------------------------------------------------
def calc_position_size(entry_price: float) -> float:
    """
    计算在给定“杠杆后下单量”下，账户实际 USD 风险固定为 ACCOUNT_USD*RISK_PCT

    返回:
        position_qty (float) —— 杠杆后下单量；同时给函数挂一个属性 risk_usd
    """
    risk_usd = ACCOUNT_USD * RISK_PCT                 # 固定风险
    position_qty = (risk_usd * LEVERAGE) / entry_price

    # 挂一个属性，供外层模板直接使用
    calc_position_size.risk_usd = round(risk_usd, 2)

    # 四舍五入到 4 位小数（合约常见精度）
    return round(position_qty, 4)
