from flask import Flask, render_template
from generate_data import get_all_analysis

app = Flask(__name__)

@app.route('/')
def index():
    try:
        ctx = get_all_analysis()
        return render_template('index.html', **ctx)
    except Exception as e:
        return f"<h1>加载失败</h1><p>{e}</p>", 500

# 不再使用 Flask 自带调试服务，Gunicorn 会作为生产服务运行
if __name__ == '__main__':
    # 仅用于本地测试，请使用 Gunicorn 启动生产服务
    app.run(debug=True, host='0.0.0.0', port=5000)
