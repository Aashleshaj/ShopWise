import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Grocery Price Comparator")

st.title("🛒 Grocery Price Comparator")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "..", "data")
DATA_FOLDER = os.path.abspath(DATA_FOLDER)

# DATA_FOLDER = "ShopWise\\data"

# ---------------------------------
# Load all CSVs from data folder
# ---------------------------------
if not os.path.exists(DATA_FOLDER):
    st.error("❌ 'data' folder not found.")
    st.stop()

csv_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]

if not csv_files:
    st.warning("⚠ No CSV files found in data folder.")
    st.stop()

all_data = []

for file in csv_files:
    store_name = os.path.splitext(file)[0].title()
    file_path = os.path.join(DATA_FOLDER, file)

    df = pd.read_csv(file_path)

    # Standardize column names
    df.columns = df.columns.str.lower().str.strip()

    # Validation
    required_cols = {"product_name", "quantity", "price"}
    if not required_cols.issubset(df.columns):
        st.error(f"❌ {file} is missing required columns.")
        st.stop()

    df["store"] = store_name
    all_data.append(df)

combined_df = pd.concat(all_data, ignore_index=True)

st.subheader("Loaded Store Data")
st.dataframe(combined_df)

# ---------------------------------
# Product & Quantity Selection
# ---------------------------------
product = st.selectbox(
    "Select Product",
    sorted(combined_df["product_name"].unique())
)

quantity = st.selectbox(
    "Select Quantity",
    sorted(
        combined_df[
            combined_df["product_name"] == product
        ]["quantity"].unique()
    )
)

# ---------------------------------
# Compare Prices
# ---------------------------------
result_df = combined_df[
    (combined_df["product_name"] == product) &
    (combined_df["quantity"] == quantity)
]

# st.dataframe(
#     combined_df.style.highlight_min(
#         subset=["price"],
#         color="lightgreen"
#     ),
#     use_container_width=True
# )

st.subheader("Price Comparison")
st.table(result_df[["store", "price"]])

cheapest = result_df.loc[result_df["price"].idxmin()]

st.success(
    f"💰 Cheapest option: **{cheapest['store']} – £{cheapest['price']}**"
)
