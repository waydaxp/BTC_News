# utils/strategy_explainer.py

def get_strategy_explanation(signal: str) -> str:
    """
    根据技术信号类型，返回对应的策略说明内容。
    """
    if not signal:
        return "暂无信号数据，建议观望。"

    if "多" in signal:
        return (
            "📋 当前策略说明：\n"
            "📈 市场状态：趋势偏强，建议轻仓试多。\n"
            "📊 仓位控制：初始不超过总仓位的20%。\n"
            "🛑 止损策略：设于 MA20 下方1.5倍 ATR。\n"
            "🎯 止盈策略：当前价格 + 2倍 ATR 或 RSI 高位背离出现。"
        )
    elif "空" in signal:
        return (
            "📋 当前策略说明：\n"
            "📉 市场状态：趋势偏弱，建议尝试空头操作。\n"
            "📊 仓位控制：初始轻仓为主，严控风险。\n"
            "🛑 止损策略：设于 MA20 上方1.5倍 ATR。\n"
            "🎯 止盈策略：当前价格 - 2倍 ATR 或 RSI 跌破支撑。"
        )
    else:
        return (
            "📋 当前策略说明：\n"
            "⏸ 市场状态：震荡区间，中性信号，暂不建议进场。\n"
            "📊 仓位控制：建议观望，避免频繁交易。\n"
            "🛑 风控建议：等待有效突破支撑/阻力位后再介入。"
        )
