from fastapi import FastAPI
import os

app = FastAPI()


@app.get("/debug/config")
def debug_config():
    return {
        "environment": dict(os.environ),
        "debug": True,
    }