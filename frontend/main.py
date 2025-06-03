import streamlit as st
import requests

st.title("Loan Timeline Comparison")

principal = st.number_input("Principal Amount", value=1000.0)
rate1 = st.number_input("Interest Rate 1 (%)", value=5.0)
rate2 = st.number_input("Interest Rate 2 (%)", value=6.0)
period = st.number_input("Loan Period (years)", value=1)

if st.button("Calculate"):
    response = requests.post(
        "http://backend:8000/calculate_loan",
        json = {
            "principal": principal,
            "rate1": rate1,
            "rate2": rate2,
            "period": period
        }
    )
    if response.status_code == 200:
        data = response.json()
        st.write(f"Total payment at rate {rate1}%: {data['total_payment_rate1']:.2f}")
        st.write(f"Total payment at rate {rate2}%: {data['total_payment_rate2']:.2f}")

    else:
        st.error("Failed to fetch data from the backend.")
