import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib
from func import DataAnalyzer, BrazilMapPlotter

sns.set(style='dark')

datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", 
                 "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]

# Load datasets
all_df = pd.read_csv("https://github.com/ashriazzr/submission-data-analyst-dicoding/tree/main/dasboard/df.csv")
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(drop=True, inplace=True)

geolocation = pd.read_csv('https://github.com/ashriazzr/submission-data-analyst-dicoding/tree/main/dasboard/geolocation.csv')
data = geolocation.drop_duplicates(subset='customer_unique_id')

# Convert columns to datetime
for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar
with st.sidebar:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image("https://github.com/ashriazzr/submission-data-analyst-dicoding/tree/main/dasboard/logo.png", width=100)
    with col3:
        st.write(' ')

    # Date Range
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

# Streamlit app
st.title("E-Commerce Public Data Analysis")

# Daily Orders Delivered
st.subheader("Daily Orders Delivered")
col1, col2 = st.columns(2)

with col1:
    total_order = daily_orders_df["order_count"].sum()
    st.markdown(f"Total Order: **{total_order}**")

with col2:
    total_revenue = daily_orders_df["revenue"].sum()
    st.markdown(f"Total Revenue: **{total_revenue}**")

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
)
axes[1].set_title("Least Sold Products")
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

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    x=review_score.index,
    y=review_score.values,
    palette="viridis",
    ax=ax
)
ax.set_title("Customer Review Scores")
st.pyplot(fig)

# Customer Demographic
st.subheader("Customer Demographic")
tab1, tab2 = st.tabs(["State", "Geolocation"])

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

with tab2:
    map_plot.plot()
