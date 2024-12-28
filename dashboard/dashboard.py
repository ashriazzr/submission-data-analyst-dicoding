import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib
from func import DataAnalyzer, BrazilMapPlotter
from streamlit_folium import folium_static
import folium

sns.set(style='dark')

# Define datetime columns
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", 
                 "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]

# Load datasets
all_df = pd.read_csv("https://raw.githubusercontent.com/ashriazzr/submission-data-analyst-dicoding/refs/heads/main/dashboard/df.csv")
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(drop=True, inplace=True)

geolocation = pd.read_csv('https://raw.githubusercontent.com/ashriazzr/submission-data-analyst-dicoding/refs/heads/main/dashboard/geolocation.csv')
data = geolocation.drop_duplicates(subset='customer_unique_id')

# Convert columns to datetime
for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])
# Data preparation
all_df[datetime_cols] = all_df[datetime_cols].apply(pd.to_datetime)
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(drop=True, inplace=True)

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.write(' ')

    # Date Range
    st.header("Filter")
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Filter data based on selected date range
main_df = all_df[(all_df["order_approved_at"] >= pd.Timestamp(start_date)) & 
                 (all_df["order_approved_at"] <= pd.Timestamp(end_date))]

# Analyze data
function = DataAnalyzer(main_df)
map_plot = BrazilMapPlotter(data, plt, mpimg, urllib, st)

daily_orders_df = function.create_daily_orders_df()
sum_spend_df = function.create_sum_spend_df()
sum_order_items_df = function.create_sum_order_items_df()
review_score, common_score = function.review_score_df()
state, most_common_state = function.create_bystate_df()
order_status, common_status = function.create_order_status()
# Filter data by date range
main_df = all_df[
    (all_df["order_approved_at"] >= pd.Timestamp(start_date)) & 
    (all_df["order_approved_at"] <= pd.Timestamp(end_date))
]

# Streamlit app
# Streamlit Title
st.title("E-Commerce Public Data Analysis")

# Daily Orders Delivered
st.subheader("Daily Orders Delivered")
col1, col2 = st.columns(2)

with col1:
    total_order = daily_orders_df["order_count"].sum()
    st.markdown(f"Total Order: **{total_order}**")
daily_orders_df = main_df.groupby(main_df["order_approved_at"].dt.date).agg(
    order_count=("order_id", "count"),
    revenue=("price", "sum")
).reset_index()

with col2:
    total_revenue = daily_orders_df["revenue"].sum()
    st.markdown(f"Total Revenue: **{total_revenue}**")
total_order = daily_orders_df["order_count"].sum()
total_revenue = daily_orders_df["revenue"].sum()

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    x=daily_orders_df["order_approved_at"],
    y=daily_orders_df["order_count"],
    marker="o",
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

# Customer Spend Money
st.subheader("Customer Spend Money")
col1, col2 = st.columns(2)

with col1:
    total_spend = sum_spend_df["total_spend"].sum()
    st.markdown(f"Total Spend: **{total_spend}**")

with col2:
    avg_spend = sum_spend_df["total_spend"].mean()
    st.markdown(f"Average Spend: **{avg_spend}**")
col1.metric("Total Orders", f"{total_order}")
col2.metric("Total Revenue", f"${total_revenue:,.2f}")

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=sum_spend_df,
    x="order_approved_at",
    y="total_spend",
    marker="o",
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

# Order Items
st.subheader("Order Items")
col1, col2 = st.columns(2)

with col1:
    total_items = sum_order_items_df["product_count"].sum()
    st.markdown(f"Total Items: **{total_items}**")

with col2:
    avg_items = sum_order_items_df["product_count"].mean()
    st.markdown(f"Average Items: **{avg_items}**")

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))

sns.barplot(
    x="product_count", 
    y="product_category_name_english", 
    data=sum_order_items_df.head(5), 
    palette="viridis", 
    ax=axes[0]
)
axes[0].set_title("Most Sold Products")
sns.barplot(
    x="product_count", 
    y="product_category_name_english", 
    data=sum_order_items_df.tail(5), 
    palette="viridis", 
    ax=axes[1]
    data=daily_orders_df, 
    x="order_approved_at", 
    y="order_count", 
    marker="o", 
    ax=ax
)
axes[1].set_title("Least Sold Products")
ax.set_title("Daily Orders Delivered")
ax.set_xlabel("Date")
ax.set_ylabel("Order Count")
st.pyplot(fig)

# Review Score
st.subheader("Review Score")
col1, col2 = st.columns(2)

with col1:
    avg_review_score = review_score.mean()
    st.markdown(f"Average Review Score: **{avg_review_score:.2f}**")

with col2:
    most_common_review_score = review_score.value_counts().idxmax()
    st.markdown(f"Most Common Review Score: **{most_common_review_score}**")
# Customer Demographic - Geolocation
st.subheader("Customer Geolocation")
geo_group = geolocation.groupby("customer_state").agg(
    customer_count=("customer_id", "count")
).reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    x=review_score.index,
    y=review_score.values,
    palette="viridis",
    data=geo_group, 
    x="customer_state", 
    y="customer_count", 
    palette="viridis", 
    ax=ax
)
ax.set_title("Customer Review Scores")
ax.set_title("Customers by State")
ax.set_xlabel("State")
ax.set_ylabel("Customer Count")
st.pyplot(fig)

# Customer Demographic
st.subheader("Customer Demographic")
tab1, tab2 = st.tabs(["State", "Geolocation"])
# Customer Demographic - Map
st.subheader("Customer Map")
customer_map = folium.Map(location=[-14.235, -51.9253], zoom_start=4)  # Brazil's coordinates

with tab1:
    most_common_state = state.customer_state.value_counts().idxmax()
    st.markdown(f"Most Common State: **{most_common_state}**")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        x=state.customer_state.value_counts().index,
        y=state.customer_count.values,
        palette="viridis",
        ax=ax
    )
    ax.set_title("Customers by State")
    st.pyplot(fig)
for _, row in geolocation.iterrows():
    folium.CircleMarker(
        location=[row["geolocation_lat"], row["geolocation_lng"]],
        radius=3,
        popup=row["customer_unique_id"],
        color="blue",
        fill=True
    ).add_to(customer_map)

with tab2:
    map_plot.plot()
folium_static(customer_map)
