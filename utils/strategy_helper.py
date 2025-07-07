def get_strategy_explanation(signal: str, symbol: str = "BTC", timeframe: str = "1h", price: float = None, rsi: float = None, atr: float = None, volume_change: float = None, funding_rate: float = None) -> str:
    """
    结构化策略输出，根据技术信号及指标生成完整的策略说明。
    参数：
    - signal: 技术信号文本
    - symbol: 币种，例如 BTC、ETH
    - timeframe: 分析周期，例如 15m, 1h, 4h
    - price: 当前价格
    - rsi: RSI 指标数值
    - atr: 平均真实波动幅度
    - volume_change: 近几根K线的成交量变化百分比（相对平均值）
    - funding_rate: 资金费率
    """
    signal = signal.strip() if signal else ""
    direction = "中性"
    bias = "震荡观望"
    
    if "做多" in signal or "偏多" in signal or "反弹" in signal:
        direction = "多"
        bias = "看涨偏多"
    elif "做空" in signal or "偏空" in signal or "回调" in signal:
        direction = "空"
        bias = "看空偏空"

    # === 技术指标判断追加 ===
    indicator_summary = []
    if rsi is not None:
        if rsi > 70:
            indicator_summary.append(f"RSI = {rsi:.1f}（超买风险）")
        elif rsi < 30:
            indicator_summary.append(f"RSI = {rsi:.1f}（超卖反弹预期）")
        else:
            indicator_summary.append(f"RSI = {rsi:.1f}（中性区域）")

    if atr is not None:
        if atr > 3:
            indicator_summary.append(f"ATR = {atr:.2f}（波动放大，需注意止损）")
        else:
            indicator_summary.append(f"ATR = {atr:.2f}（波动收敛，等待突破）")

    if volume_change is not None:
        if volume_change > 10:
            indicator_summary.append(f"成交量明显放大（+{volume_change:.1f}%）")
        elif volume_change < -10:
            indicator_summary.append(f"成交量大幅萎缩（{volume_change:.1f}%）")

    if funding_rate is not None:
        if abs(funding_rate) > 0.01:
            directionality = "多头拥挤" if funding_rate > 0 else "空头拥挤"
            indicator_summary.append(f"资金费率 = {funding_rate:.4f}（{directionality}）")

    summary_text = "\n• ".join(indicator_summary)

    explanation = f"""📊 技术分析综述（{symbol}/{timeframe}）

• 当前信号为：{signal if signal else "无明确信号"}。
• 当前判断倾向：{bias}
"""

    if summary_text:
        explanation += f"• 指标评估：\n• {summary_text}\n"

    explanation += f"""
🔍 策略建议（未来 {timeframe}）

| 情况 | 行动建议 |
|------|----------|
"""
    if direction == "多":
        explanation += (
            "| **守住支撑 & 成交量回暖** | 建议顺势做多，目标设在前高阻力附近，止损设在支撑位下方。 |\n"
            "| **未能突破关键区或成交量不足** | 建议观望，等待确认。 |\n"
        )
    elif direction == "空":
        explanation += (
            "| **跌破支撑伴随放量** | 可考虑做空，止盈设于下方支撑，止损设在关键阻力上方。 |\n"
            "| **回踩确认失败或走势反转** | 建议观望或止盈退出空单。 |\n"
        )
    else:
        explanation += (
            "| **震荡整理 & 成交量萎缩** | 建议观望，等待放量突破关键位再入场。 |\n"
            "| **快速放量突破** | 可择机顺势追单，结合风控建仓。 |\n"
        )

    explanation += f"""
✅ 结论推荐
• 当前偏向：{bias}。
• 保守策略：等待确认支撑/阻力区有效，再入场。
• 激进策略：结合成交量或K线形态择机入场，严格风控。

⚠️ 风险提示
• 请务必设置止损，控制仓位，防止强平风险。
• 信号基于程序自动判断，需结合实际盘面与资金流动态综合决策。
• 留意资金费率变化，过高时可能产生额外持仓成本。

📌 本策略分析为自动化生成，仅供参考，不构成投资建议。
"""
    return explanation
