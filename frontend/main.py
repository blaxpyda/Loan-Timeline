import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.title("Loan Timeline Comparison")

principal = st.number_input("Principal Amount", value=1000.0)
rate1 = st.number_input("Interest Rate 1 (%)", value=5.0)
rate2 = st.number_input("Interest Rate 2 (%)", value=6.0)
period = st.number_input("Loan Period (years)", value=1)

if st.button("Calculate"):
    url = "http://backend:8000/calculate_loan"
    data = {"principal": principal, "rate1": rate1, "rate2": rate2, "period": period}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        st.subheader(
            f"Total Payment (Rate 1 - {rate1}%: {result['total_payment_rate1']:.2f})"
        )
        st.subheader(
            f"Total Payment (Rate 2 - {rate2}%: {result['total_payment_rate2']:.2f})"
        )

        st.markdown("### Amortization Schedule (Rate 1)")
        df1 = pd.DataFrame(result["amortization_schedule_rate1"])
        st.dataframe(df1)

        st.markdown("### Amortization Schedule (Rate 2)")
        df2 = pd.DataFrame(result["amortization_schedule_rate2"])
        st.dataframe(df2)

        # Plot comparison of loan balances
        fig, ax = plt.subplots()
        ax.plot(
            df1["payment_number"],
            df1["remaining_balance"],
            label=f"Rate 1 ({rate1}%)",
            color="blue",
        )
        ax.plot(
            df2["payment_number"],
            df2["remaining_balance"],
            label=f"Rate 2 ({rate2}%)",
            color="orange",
        )
        ax.set_xlabel("Payment Number")
        ax.set_ylabel("Remaining Balance")
        ax.set_title("Loan Balance Over Time")
        ax.legend()
        st.pyplot(fig)
    else:
        st.error("Failed to fetch data from the backend.")
