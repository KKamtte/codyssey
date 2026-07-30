import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS memos (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/memo", methods=["POST"])
def save_memo():
    content = request.json.get("content")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO memos (content) VALUES (%s)", (content,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "저장 완료"}), 201

@app.route("/memo", methods=["GET"])
def get_memos():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, content, created_at FROM memos ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([
        {"id": r[0], "content": r[1], "created_at": str(r[2])}
        for r in rows
    ])

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("FLASK_PORT", 5000))
    app.run(host="0.0.0.0", port=port)