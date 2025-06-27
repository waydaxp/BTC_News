from jinja2 import Environment, FileSystemLoader
from generate_data import get_all_analysis
from datetime import datetime
import pytz

def generate_html():
    # 获取所有数据
    data = get_all_analysis()

    # 转为北京时间（UTC+8）
    # 获取当前 UTC 时间并转换为北京时间
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    beijing_time = utc_now.astimezone(pytz.timezone("Asia/Shanghai"))
    data["last_updated"] = beijing_time.strftime("%Y-%m-%d %H:%M 北京时间")

    # 加载模板文件
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("index_template.html")

    # 渲染 HTML 并写入文件
    rendered = template.render(**data, update_time=beijing_time)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(rendered)  # ✅ 正确的变量名

if __name__ == "__main__":
    generate_html()
