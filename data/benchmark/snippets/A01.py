from fastapi import FastAPI, Query
import sqlite3

app = FastAPI()


@app.get("/search")
def search(q: str = Query("")):
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()

    query = f"SELECT * FROM products WHERE name LIKE '%{q}%'"
    cursor.execute(query)

    rows = cursor.fetchall()
    conn.close()

    return {"results": rows}