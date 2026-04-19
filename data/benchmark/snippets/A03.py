from fastapi import FastAPI

app = FastAPI()


@app.get("/admin/stats")
def admin_stats():
    return {
        "users": 1042,
        "revenue": 182300,
        "active_sessions": 87,
    }