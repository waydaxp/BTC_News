<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <title>Crypto 技术面仪表盘</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta http-equiv="refresh" content="60" />
  <style>
    body {
      font-family: "Segoe UI", system-ui, sans-serif;
      font-size: 16px;
      background: #f7f9fb;
      color: #333;
      margin: 0;
      padding: 0;
    }
    .card {
      background: #ffffff;
      border-left: 6px solid #2ecc71;
      margin: 20px auto;
      padding: 20px 24px;
      width: 90%;
      max-width: 900px;
      border-radius: 8px;
      box-shadow: 0 1px 6px rgba(0,0,0,0.06);
    }
    .title {
      font-size: 24px;
      font-weight: bold;
      margin-bottom: 14px;
      display: flex;
      align-items: center;
    }
    .title.eth { color: #6a1b9a; }
    .title.btc { color: #1565c0; }
    .title::before {
      content: "📈";
      margin-right: 8px;
    }
    .metric {
      margin-bottom: 6px;
      line-height: 1.6;
    }
    .metric span.label {
      display: inline-block;
      min-width: 100px;
      font-weight: bold;
      color: #333;
    }
    .strategy-section {
      margin-top: 10px;
      background: #fdfdfd;
      padding: 12px 16px;
      border-left: 4px solid #f39c12;
      border-radius: 5px;
      font-size: 15px;
      white-space: pre-line;
    }
    .update {
      font-size: 13px;
      color: #777;
      text-align: right;
      margin-top: -10px;
    }
  </style>
</head>
<body>

  {% set periods = ["15m", "1h", "4h"] %}

  {% for tf in periods %}
  <div class="card">
    <div class="title btc">BTC {{ tf }} 技术指标</div>
    <div class="metric"><span class="label">当前价格:</span> {{ attribute(_context, "btc_price_" ~ tf) }}</div>
    <div class="metric"><span class="label">MA20:</span> {{ attribute(_context, "btc_ma20_" ~ tf) }}</div>
    <div class="metric"><span class="label">RSI:</span> {{ attribute(_context, "btc_rsi_" ~ tf) }}</div>
    <div class="metric"><span class="label">ATR:</span> {{ attribute(_context, "btc_atr_" ~ tf) }}</div>
    <div class="metric"><span class="label">成交量:</span> {{ attribute(_context, "btc_volume_" ~ tf) }}</div>
    <div class="metric"><span class="label">支撑区间:</span> {{ attribute(_context, "btc_support_" ~ tf) }}</div>
    <div class="metric"><span class="label">阻力区间:</span> {{ attribute(_context, "btc_resistance_" ~ tf) }}</div>
    <div class="metric"><span class="label">资金费率:</span> {{ attribute(_context, "btc_funding_" ~ tf) }}</div>
  </div>

  <div class="card">
    <div class="title">📊 BTC {{ tf }} 策略建议</div>
    <div class="metric"><span class="label">信号:</span> {{ attribute(_context, "btc_signal_" ~ tf) }}</div>
    <div class="metric"><span class="label">止盈价:</span> {{ attribute(_context, "btc_tp_" ~ tf) }}</div>
    <div class="metric"><span class="label">止损价:</span> {{ attribute(_context, "btc_sl_" ~ tf) }}</div>
    <div class="strategy-section">{{ attribute(_context, "btc_strategy_note_" ~ tf) }}</div>
  </div>
  {% endfor %}

  <!-- 恐惧与贪婪指数 -->
  <div class="card">
    <div class="title">😨/😊 恐惧与贪婪指数</div>
    <div class="metric"><span class="label">当前值:</span> {{ fg_idx }}（{{ fg_txt }}）{{ fg_emoji }}</div>
    <div class="metric"><span class="label">时间:</span> {{ fg_ts }}</div>
    <div class="metric"><span class="label">说明:</span> 指数 < 50 为恐惧，> 50 为贪婪</div>
  </div>

  <!-- 页面更新时间 -->
  <div class="card update">
    页面更新时间：{{ page_update }}（北京时间）｜每 60 秒自动刷新
  </div>

</body>
</html>
