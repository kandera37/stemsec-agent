from fastapi import FastAPI, Query

app = FastAPI()

INVOICES = {
    1: {"owner_id": 10, "amount": 120},
    2: {"owner_id": 20, "amount": 300},
}


@app.get("/invoice")
def get_invoice(invoice_id: int = Query(...), current_user_id: int = Query(...)):
    invoice = INVOICES[invoice_id]
    return invoice