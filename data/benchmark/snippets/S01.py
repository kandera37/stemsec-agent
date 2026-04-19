from flask import Flask, request
import sqlite3

app = Flask(__name__)


@app.route("/search")
def search():
    q = request.args.get("q", "")
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE name LIKE ?", (f"%{q}%",))
    rows = cursor.fetchall()
    conn.close()

    return {"results": rows}