# gunicorn_config.py
bind = "0.0.0.0:8000"
workers = 4
timeout = 120
accesslog = "-"
errorlog = "-"
