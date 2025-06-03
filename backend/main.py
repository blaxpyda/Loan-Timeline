from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class LoanDetails(BaseModel):
    principal: float
    rate1: float
    rate2: float
    period: int

@app.post("/calculate_loan")
def calculate_loan(details: LoanDetails):
    p = details.principal
    r1 = details.rate1 / 100
    r2 = details.rate2 / 100
    n = details.period

    total_payment_rate1 = p * (1 + r1 * n)
    total_payment_rate2 = p * (1 + r2 * n)

    return {
        "total_payment_rate1": total_payment_rate1,
        "total_payment_rate2": total_payment_rate2
    }