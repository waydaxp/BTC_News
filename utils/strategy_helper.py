# utils/strategy_helper.py

def get_strategy_explanation(signal: str) -> str:
    if "多" in signal:
        return (
            "市场状态：趋势偏强，建议轻仓试多。\n"
            "仓位建议：初始不超过总仓位的20%。\n"
            "止损设于 MA20 下方1.5倍ATR，止盈为当前价+2倍ATR或RSI高位背离出现。"
        )
    elif "空" in signal:
        return (
            "市场状态：趋势偏弱，建议尝试空头操作。\n"
            "仓位建议：轻仓为主，严控风险。\n"
            "止损设于 MA20 上方1.5倍ATR，止盈为当前价-2倍ATR或RSI跌破支撑。"
        )
    else:
        return (
            "市场状态：中性震荡，暂不建议进场。\n"
            "仓位建议：观望为主，避免频繁交易。\n"
            "风险控制：等待价格突破区间后再计划进场。"
        )
