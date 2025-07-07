# strategy_helper.py

def get_strategy_explanation(signal: str, tf: str = "1h", price: float = None,
                              support_range: tuple = None, resistance_range: tuple = None,
                              volume_rising: bool = False) -> str:
    """
    返回结构化策略说明，支持动态区间建议。
    参数：
        - signal: 技术信号（如 "做多"、"做空"、"震荡"）
        - tf: 时间周期（"15m", "1h", "4h"）
        - price: 当前价格
        - support_range: 支撑区间（元组）
        - resistance_range: 压力区间（元组）
        - volume_rising: 成交量是否回暖
    """
    explain = []
    explain.append(f"⏱ 当前周期：{tf.upper()}，价格：${price if price else '—'}")

    if signal is None or signal.strip() == "":
        explain.append("📭 暂无明确信号，建议观望等待趋势明确。")
        return "\n".join(explain)

    if signal in ["震荡", "中性"]:
        explain.append("\n🧠 技术分析综述：")
        explain.append("• 价格围绕 MA20 波动，暂无趋势确认。")
        if support_range and resistance_range:
            explain.append(f"• 支撑区间：${support_range[0]}–${support_range[1]}，阻力区间：${resistance_range[0]}–${resistance_range[1]}。")
        explain.append("\n🔍 策略建议：")
        explain.append("• 建议观望，等待放量突破关键支撑/阻力再入场。")
        explain.append("• 若突破上轨伴随放量，可择机做多，反之做空。")

    elif "做多" in signal:
        explain.append("\n🧠 技术分析综述：")
        explain.append("• RSI 上行、价格守稳 EMA 支撑，有望继续上攻。")
        if support_range:
            explain.append(f"• 关键支撑：${support_range[0]}–${support_range[1]}。")
        if resistance_range:
            explain.append(f"• 若突破阻力区 ${resistance_range[0]}–${resistance_range[1]}，目标可见更高位。")

        explain.append("\n🔍 短线策略建议：")
        if volume_rising:
            explain.append("• 成交量回暖，建议小仓位做多。")
        else:
            explain.append("• 成交量未明显放大，建议谨慎跟随。")
        if support_range:
            explain.append(f"• 止损建议设在支撑下方，如 ${support_range[0] - 10}。")
        if resistance_range:
            explain.append(f"• 初步止盈可设至 ${resistance_range[1]} 或更高。")

    elif "做空" in signal:
        explain.append("\n🧠 技术分析综述：")
        explain.append("• RSI 回落，价格失守短期均线支撑。")
        if resistance_range:
            explain.append(f"• 压力区：${resistance_range[0]}–${resistance_range[1]}。")
        if support_range:
            explain.append(f"• 若跌破支撑区 ${support_range[0]}–${support_range[1]}，下方空间打开。")

        explain.append("\n🔍 短线策略建议：")
        if volume_rising:
            explain.append("• 若跌破支撑且放量，建议短线做空。")
        else:
            explain.append("• 未出现放量，不宜盲目追空。")
        if resistance_range:
            explain.append(f"• 止损设在 ${resistance_range[1] + 10} 上方。")
        if support_range:
            explain.append(f"• 止盈可先看 ${support_range[0]} 或以下位置。")

    else:
        explain.append("⚠️ 当前信号未匹配标准策略，建议结合盘面灵活应对。")

    explain.append("\n⚠️ 风险提示：合约交易波动大，请控制杠杆并设置止损。")
    return "\n".join(explain)
