from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/hello", response_class=HTMLResponse)
def hello(name: str = Query("")):
    return f"<h1>Hello, {name}!</h1>"