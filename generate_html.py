# generate_html.py
"""
拉取最新数据 → 用 Jinja2 渲染 HTML → 写入 index.html
"""

from generate_data import get_all_analysis
from jinja2 import Template

# 1. 获取 BTC / ETH / 宏观 / 情绪 等所有字段
ctx = get_all_analysis()          # ctx == dict

# 2. 读取 Jinja2 模板
with open("index_template.html", encoding="utf-8") as f:
    tpl = Template(f.read())

# 3. 渲染
html = tpl.render(**ctx)

# 4. 输出静态页面
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ index.html 已生成 ——", ctx["update_time"])
