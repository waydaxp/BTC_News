import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

def generate_html():
    # 加载 JSON 数据
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # 处理更新时间戳（Unix → 可读格式）
    timestamp = data.get("update_time")
    if isinstance(timestamp, int):
        data["update_time"] = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M UTC")
    elif not timestamp:
        data["update_time"] = "未知时间"

    # 加载模板引擎
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("index_template.html")

    # 渲染 HTML
    rendered_html = template.render(**data)

    # 写入 HTML 文件
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(rendered_html)

    print("✅ 成功生成 index.html")

if __name__ == "__main__":
    generate_html()
