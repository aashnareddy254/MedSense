import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="MedSense AI",
    page_icon="💊",
    layout="wide"
)

# Load Inventory
df = pd.read_csv("inventory.csv")

# Session Sales History
if "sales_history" not in st.session_state:
    st.session_state.sales_history = []

# Header
st.title("💊 MedSense AI")
st.subheader("AI-Powered Pharmacy Decision Intelligence")

st.divider()

# KPIs

total_medicines = len(df)
total_stock = df["Quantity"].sum()
low_stock = len(df[df["Quantity"] < 20])
expiry_risk = len(df[df["Expiry_Days"] < 30])
inventory_value = (df["Quantity"] * df["Price"]).sum()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Medicines", total_medicines)
col2.metric("Total Stock", total_stock)
col3.metric("Low Stock", low_stock)
col4.metric("Expiry Risk", expiry_risk)
col5.metric("Inventory Value ₹", round(inventory_value))

st.divider()

# Inventory

st.subheader("📦 Inventory")

search = st.text_input("Search Medicine")

if search:
    filtered_df = df[
        df["Medicine"].str.contains(search, case=False)
    ]
else:
    filtered_df = df

st.dataframe(
    filtered_df,
    use_container_width=True
)

st.divider()

# Alerts

st.subheader("🚨 Smart Alerts")

low_stock_items = df[df["Quantity"] < 20]

for _, row in low_stock_items.iterrows():
    st.error(
        f"{row['Medicine']} is running low ({row['Quantity']} units left)"
    )

expiry_items = df[df["Expiry_Days"] < 30]

for _, row in expiry_items.iterrows():
    st.warning(
        f"{row['Medicine']} expires in {row['Expiry_Days']} days"
    )

st.divider()

# Reorder Suggestions

st.subheader("📦 Reorder Recommendations")

reorder = df[df["Quantity"] < 20]

if len(reorder) > 0:
    st.dataframe(
        reorder[["Medicine", "Quantity"]],
        use_container_width=True
    )
else:
    st.success("No medicines require reordering")

st.divider()

# Billing System

st.subheader("🧾 Billing System")

medicine = st.selectbox(
    "Select Medicine",
    df["Medicine"]
)

qty_sold = st.number_input(
    "Quantity Sold",
    min_value=1,
    value=1
)

if st.button("Generate Bill"):

    current_stock = df.loc[
        df["Medicine"] == medicine,
        "Quantity"
    ].values[0]

    price = df.loc[
        df["Medicine"] == medicine,
        "Price"
    ].values[0]

    if qty_sold > current_stock:

        st.error(
            f"Only {current_stock} units available"
        )

    else:

        amount = qty_sold * price

        df.loc[
            df["Medicine"] == medicine,
            "Quantity"
        ] -= qty_sold

        df.to_csv(
            "inventory.csv",
            index=False
        )

        st.session_state.sales_history.append({
            "Medicine": medicine,
            "Quantity": qty_sold,
            "Amount": amount
        })

        st.success("Bill Generated Successfully")

        st.write("### Invoice")
        st.write(f"Medicine: {medicine}")
        st.write(f"Quantity: {qty_sold}")
        st.write(f"Amount: ₹{amount}")

        st.rerun()

st.divider()

# Sales History

st.subheader("📋 Sales History")

if len(st.session_state.sales_history) > 0:

    sales_df = pd.DataFrame(
        st.session_state.sales_history
    )

    st.dataframe(
        sales_df,
        use_container_width=True
    )

else:
    st.info("No sales recorded yet")

st.divider()

# Demand Forecast

st.subheader("📈 Demand Forecast")

forecast = pd.DataFrame({
    "Week":[1,2,3,4,5,6],
    "Predicted Demand":[100,120,140,160,175,190]
})

st.line_chart(
    forecast.set_index("Week")
)

st.divider()

# AI Assistant

st.subheader("🤖 AI Assistant")

question = st.text_input(
    "Ask MedSense AI"
)

if question:

    q = question.lower()

    if "reorder" in q:

        st.success(
            "Recommended reorder: Crocin, Dolo650, VitaminC"
        )

    elif "expiry" in q:

        st.success(
            "Expiry risk medicines: VitaminC, Dolo650, Crocin"
        )

    elif "low stock" in q:

        st.success(
            "Low stock medicines detected. Please reorder soon."
        )

    elif "inventory value" in q:

        st.success(
            f"Current inventory value is ₹{round(inventory_value)}"
        )

    else:

        st.success(
            "Inventory appears stable. Monitor low stock and expiry alerts."
        )
        
