import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="MedSense AI",
    layout="wide"
)

st.title("💊 MedSense AI")
st.subheader("Pharmacy Decision Intelligence Dashboard")

df = pd.read_csv("inventory.csv")

# KPIs

total_medicines = len(df)

total_stock = df["Quantity"].sum()

low_stock = len(df[df["Quantity"] < 20])

expiry_risk = len(df[df["Expiry_Days"] < 30])

stock_value = (df["Quantity"] * df["Price"]).sum()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Medicines", total_medicines)
col2.metric("Total Stock", total_stock)
col3.metric("Low Stock", low_stock)
col4.metric("Expiry Risk", expiry_risk)
col5.metric("Inventory Value ₹", stock_value)

st.divider()

# Inventory Table

st.subheader("Inventory")

st.dataframe(df, use_container_width=True)

st.divider()

# Alerts

st.subheader("🚨 Smart Alerts")

low_stock_items = df[df["Quantity"] < 20]

for _, row in low_stock_items.iterrows():
    st.error(
        f"{row['Medicine']} is running low ({row['Quantity']} units)"
    )

expiry_items = df[df["Expiry_Days"] < 30]

for _, row in expiry_items.iterrows():
    st.warning(
        f"{row['Medicine']} expires in {row['Expiry_Days']} days"
    )

st.divider()

# Reorder Recommendations

st.subheader("📦 Reorder Recommendations")

reorder = df[df["Quantity"] < 20]

if len(reorder) > 0:
    st.dataframe(
        reorder[["Medicine", "Quantity"]],
        use_container_width=True
    )

st.divider()

# Business Health Score

score = 100

score -= low_stock * 5
score -= expiry_risk * 5

score = max(score, 0)

st.subheader("📈 Business Health Score")

st.progress(score / 100)

st.success(f"Health Score: {score}/100")

st.divider()

# Forecasting

st.subheader("📊 Demand Forecast")

forecast = pd.DataFrame({
    "Week":[1,2,3,4,5],
    "Predicted Demand":[100,115,130,145,160]
})

st.line_chart(
    forecast.set_index("Week")
)

st.divider()

# Simple AI Assistant

st.subheader("🤖 AI Assistant")

question = st.text_input(
    "Ask a question"
)

if question:

    if "reorder" in question.lower():
        st.success(
            "Recommended reorder: Crocin, Dolo650 and VitaminC"
        )

    elif "expiry" in question.lower():
        st.success(
            "High expiry risk medicines: VitaminC, Dolo650, Crocin"
        )

    else:
        st.success(
            "Inventory is stable. Monitor low stock medicines."
        )
