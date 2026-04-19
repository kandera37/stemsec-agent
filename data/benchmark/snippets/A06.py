from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class CalcRequest(BaseModel):
    expression: str


@app.post("/calculate")
def calculate(payload: CalcRequest):
    result = eval(payload.expression)
    return {"result": result}