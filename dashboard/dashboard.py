import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from streamlit_folium import folium_static
import folium

sns.set(style='dark')

# Define datetime columns
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", 
                 "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]

# Load datasets
all_df = pd.read_csv("https://raw.githubusercontent.com/ashriazzr/submission-data-analyst-dicoding/refs/heads/main/dashboard/df.csv")
geolocation = pd.read_csv('https://raw.githubusercontent.com/ashriazzr/submission-data-analyst-dicoding/refs/heads/main/dashboard/geolocation.csv')

# Data preparation
all_df[datetime_cols] = all_df[datetime_cols].apply(pd.to_datetime)
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(drop=True, inplace=True)

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    st.header("Filter")
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Filter data by date range
main_df = all_df[
    (all_df["order_approved_at"] >= pd.Timestamp(start_date)) & 
    (all_df["order_approved_at"] <= pd.Timestamp(end_date))
]

# Streamlit Title
st.title("E-Commerce Public Data Analysis")

# Daily Orders Delivered
st.subheader("Daily Orders Delivered")
daily_orders_df = main_df.groupby(main_df["order_approved_at"].dt.date).agg(
    order_count=("order_id", "count"),
    revenue=("price", "sum")
).reset_index()

total_order = daily_orders_df["order_count"].sum()
total_revenue = daily_orders_df["revenue"].sum()

col1, col2 = st.columns(2)
col1.metric("Total Orders", f"{total_order}")
col2.metric("Total Revenue", f"${total_revenue:,.2f}")

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=daily_orders_df, 
    x="order_approved_at", 
    y="order_count", 
    marker="o", 
    ax=ax
)
ax.set_title("Daily Orders Delivered")
ax.set_xlabel("Date")
ax.set_ylabel("Order Count")
st.pyplot(fig)

# Customer Demographic - Geolocation
st.subheader("Customer Geolocation")
geo_group = geolocation.groupby("customer_state").agg(
    customer_count=("customer_id", "count")
).reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    data=geo_group, 
    x="customer_state", 
    y="customer_count", 
    palette="viridis", 
    ax=ax
)
ax.set_title("Customers by State")
ax.set_xlabel("State")
ax.set_ylabel("Customer Count")
st.pyplot(fig)

# Customer Demographic - Map
st.subheader("Customer Map")
customer_map = folium.Map(location=[-14.235, -51.9253], zoom_start=4)  # Brazil's coordinates

for _, row in geolocation.iterrows():
    folium.CircleMarker(
        location=[row["geolocation_lat"], row["geolocation_lng"]],
        radius=3,
        popup=row["customer_unique_id"],
        color="blue",
        fill=True
    ).add_to(customer_map)

folium_static(customer_map)
