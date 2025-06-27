from jinja2 import Template
from datetime import datetime
import yfinance as yf

# 获取 BTC & ETH 数据
btc = yf.Ticker("BTC-USD").history(period="1d", interval="1m")
eth = yf.Ticker("ETH-USD").history(period="1d", interval="1m")

btc_price = btc['Close'].iloc[-1]
eth_price = eth['Close'].iloc[-1]
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 读取模板
with open("data/template.html", "r", encoding="utf-8") as f:
    template = Template(f.read())

# 渲染页面
rendered = template.render(
    btc_price=round(btc_price, 2),
    eth_price=round(eth_price, 2),
    update_time=now
)

# 输出到 index.html
with open("index.html", "w", encoding="utf-8") as f:
    f.write(rendered)
