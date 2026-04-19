from fastapi import FastAPI, Header
import logging

app = FastAPI()
logger = logging.getLogger(__name__)


@app.get("/profile")
def profile(authorization: str = Header(default="")):
    logger.info("Authorization header: %s", authorization)
    return {"message": "ok"}