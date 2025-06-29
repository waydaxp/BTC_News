# generate_html.py
from generate_data import get_all_analysis
from pathlib import Path

TEMPLATE = Path("index_template.html").read_text(encoding="utf-8")
html = TEMPLATE.format(**get_all_analysis())
Path("index.html").write_text(html, encoding="utf-8")
print("✅ index.html 已生成")
