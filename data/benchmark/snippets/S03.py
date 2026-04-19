from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import html

app = FastAPI()


@app.get("/preview", response_class=HTMLResponse)
def preview(text: str = Query("")):
    safe_text = html.escape(text)
    return f"<div>{safe_text}</div>"