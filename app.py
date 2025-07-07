from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Flask 服务正常运行！"
