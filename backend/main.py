from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


class LoanDetails(BaseModel):
    principal: float
    rate1: float
    rate2: float
    period: int


class AmortizationEntry(BaseModel):
    payment_number: int
    payment_amount: float
    principal_payment: float
    interest_payment: float
    remaining_balance: float


class LoanAmortizationResponse(BaseModel):
    total_payment_rate1: float
    total_payment_rate2: float
    amortization_schedule_rate1: List[AmortizationEntry]
    amortization_schedule_rate2: List[AmortizationEntry]


def calculate_amortization(principal, annual_rate, period):
    r = annual_rate / 100 / 12
    n = period
    p = principal

    if r == 0:
        monthly_payment = p / n
    else:
        monthly_payment = p * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

    schedule = []
    balance = p

    for i in range(1, n + 1):
        interest = balance * r
        principal_payment = monthly_payment - interest
        balance -= principal_payment
        schedule.append(
            AmortizationEntry(
                payment_number=i,
                payment_amount=monthly_payment,
                principal_payment=principal_payment,
                interest_payment=interest,
                remaining_balance=max(
                    balance, 0
                ),  # Ensure balance does not go negative
            )
        )

    total_payment = monthly_payment * n
    return total_payment, schedule


@app.post("/calculate_loan", response_model=LoanAmortizationResponse)
def calculate_loan(details: LoanDetails):
    total_payment_rate1, schedule_rate1 = calculate_amortization(
        details.principal, details.rate1, details.period * 12
    )
    total_payment_rate2, schedule_rate2 = calculate_amortization(
        details.principal, details.rate2, details.period * 12
    )

    return LoanAmortizationResponse(
        total_payment_rate1=total_payment_rate1,
        total_payment_rate2=total_payment_rate2,
        amortization_schedule_rate1=schedule_rate1,
        amortization_schedule_rate2=schedule_rate2,
    )
