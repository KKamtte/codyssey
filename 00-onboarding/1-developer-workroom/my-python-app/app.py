# app.py
from flask import Flask
import os

app = Flask(__name__)
DATA_FILE = "/app/data/hello.txt"

@app.route('/')
def hello():
    return "<h1>Ubuntu + Python Multi-stage Build Success!</h1>"

@app.route('/write/<content>')
def write_file(content):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "a") as f:
        f.write(content + "\n")
    return f"Saved: {content}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
