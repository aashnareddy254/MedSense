import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="MedSense AI", layout="wide")

st.title("💊 MedSense AI")
st.subheader("AI-Powered Pharmacy Decision Intelligence")

uploaded_file = st.file_uploader(
    "Upload Inventory CSV",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.success("Inventory Loaded")

    st.dataframe(df)

    total_stock = df["Quantity"].sum()

    low_stock = len(df[df["Quantity"] < 20])

    st.metric("Total Stock", total_stock)
    st.metric("Low Stock Medicines", low_stock)

    st.subheader("Inventory")

    st.bar_chart(df.set_index("Medicine")["Quantity"])

else:
    st.info("Upload inventory CSV to begin")
    