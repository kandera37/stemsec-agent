from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()


class FetchRequest(BaseModel):
    url: str


@app.post("/fetch")
def fetch_remote_page(payload: FetchRequest):
    response = requests.get(payload.url, timeout=5)
    return {"status_code": response.status_code, "body": response.text[:200]}