from fastapi import FastAPI, Query
import os
import sqlite3

app = FastAPI()

BASE_DIR = "exports"


@app.get("/export")
def export_report(file: str = Query("report.txt"), user_id: int = Query(...)):
    conn = sqlite3.connect("reports.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reports WHERE owner_id = ?", (user_id,))
    reports = cursor.fetchall()
    conn.close()

    path = os.path.join(BASE_DIR, file)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    return {"reports": reports, "preview": content[:100]}