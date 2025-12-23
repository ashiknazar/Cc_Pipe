import streamlit as st
import pandas as pd
from pyspark.sql import SparkSession
import time

# Spark session
spark = (
    SparkSession.builder
    .appName("CryptoStreamlitApp")
    .getOrCreate()
)

st.title("Live Crypto Prices Dashboard")

# Sidebar
st.sidebar.markdown("Refresh interval in seconds")
refresh_interval = st.sidebar.slider("Refresh interval", 1, 10, 5)

selected_asset = st.sidebar.selectbox(
    "Select coin for change chart",
    ["bitcoin", "ethereum", "cardano", "solana", "dogecoin"]
)

# Placeholders (CRITICAL)
price_chart_placeholder = st.empty()
change_chart_placeholder = st.empty()

parquet_path = "/home/ashik/codes/Cc_pipe/data/crypto_prices_parquet"

while True:
    try:
        df = spark.read.parquet(parquet_path)
        pdf = df.toPandas()

        if not pdf.empty:
            # -----------------------
            # MAIN PRICE CHART
            # -----------------------
            chart_data = (
                pdf
                .pivot(index="event_time", columns="asset", values="price_usd")
                .sort_index()
            )

            price_chart_placeholder.line_chart(chart_data)

            # -----------------------
            # SINGLE COIN CHANGE CHART
            # -----------------------
            asset_df = (
                pdf[pdf["asset"] == selected_asset]
                .sort_values("event_time")
                .set_index("event_time")
            )

            asset_df["price_change"] = asset_df["price_usd"].diff()

            with change_chart_placeholder.container():
                st.subheader(f"{selected_asset.capitalize()} – Price Change")
                st.line_chart(asset_df["price_change"])

    except Exception as e:
        st.error(f"Error: {e}")

    time.sleep(refresh_interval)
