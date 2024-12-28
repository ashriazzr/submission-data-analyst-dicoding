import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from func import DataAnalyzer, BrazilMapPlotter

sns.set(style="darkgrid")

# Kolom datetime
datetime_cols = [
    "order_approved_at", "order_delivered_carrier_date", 
    "order_delivered_customer_date", "order_estimated_delivery_date", 
    "order_purchase_timestamp", "shipping_limit_date"
]

# Load datasets
@st.cache_data
def load_data():
    all_df = pd.read_csv(
        "https://raw.githubusercontent.com/ashriazzr/submission-data-analyst-dicoding/main/dashboard/df.csv"
    )
    geolocation = pd.read_csv(
        "https://raw.githubusercontent.com/ashriazzr/submission-data-analyst-dicoding/main/dashboard/geolocation.csv"
    )
    return all_df, geolocation

all_df, geolocation = load_data()

# Data Preparation
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(drop=True, inplace=True)

# Konversi kolom datetime
for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col], errors="coerce")

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar - Date Range
with st.sidebar:
    st.header("Filter")
    start_date, end_date = st.date_input(
        label="Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date,
    )

# Filter data berdasarkan rentang tanggal
if start_date and end_date:
    main_df = all_df[
        (all_df["order_approved_at"] >= pd.Timestamp(start_date)) & 
        (all_df["order_approved_at"] <= pd.Timestamp(end_date))
    ]
else:
    st.error("Invalid date range. Please select a valid range.")
    st.stop()

# Analisis Data
function = DataAnalyzer(main_df)
map_plot = BrazilMapPlotter(geolocation, plt, st)

daily_orders_df = function.create_daily_orders_df()
sum_spend_df = function.create_sum_spend_df()
sum_order_items_df = function.create_sum_order_items_df()
review_score, common_score = function.review_score_df()
state, most_common_state = function.create_bystate_df()
order_status, common_status = function.create_order_status()

# Streamlit App
st.title("E-Commerce Public Data Analysis")

# Daily Orders Delivered
st.subheader("Daily Orders Delivered")
total_order = daily_orders_df["order_count"].sum()
total_revenue = daily_orders_df["revenue"].sum()

st.write(f"Total Orders: **{total_order}**")
st.write(f"Total Revenue: **${total_revenue:,.2f}**")

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=daily_orders_df,
    x="order_approved_at",
    y="order_count",
    marker="o",
    color="#2196F3",
    linewidth=2,
    ax=ax,
)
ax.set_title("Daily Orders Delivered", fontsize=16)
ax.set_xlabel("Date", fontsize=14)
ax.set_ylabel("Order Count", fontsize=14)
plt.xticks(rotation=45)
st.pyplot(fig)

# Customer Spend Money
st.subheader("Customer Spend Money")
total_spend = sum_spend_df["total_spend"].sum()
avg_spend = sum_spend_df["total_spend"].mean()

st.write(f"Total Spend: **${total_spend:,.2f}**")
st.write(f"Average Spend: **${avg_spend:,.2f}**")

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=sum_spend_df,
    x="order_approved_at",
    y="total_spend",
    marker="o",
    color="#FF9800",
    linewidth=2,
    ax=ax,
)
ax.set_title("Customer Spend Over Time", fontsize=16)
ax.set_xlabel("Date", fontsize=14)
ax.set_ylabel("Total Spend", fontsize=14)
plt.xticks(rotation=45)
st.pyplot(fig)

# Order Items
st.subheader("Order Items")
total_items = sum_order_items_df["product_count"].sum()
avg_items = sum_order_items_df["product_count"].mean()

st.write(f"Total Items Sold: **{total_items}**")
st.write(f"Average Items per Order: **{avg_items:.2f}**")

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))
sns.barplot(
    data=sum_order_items_df.nlargest(5, "product_count"),
    x="product_count",
    y="product_category_name_english",
    palette="coolwarm",
    ax=axes[0],
)
axes[0].set_title("Top 5 Sold Products", fontsize=14)
sns.barplot(
    data=sum_order_items_df.nsmallest(5, "product_count"),
    x="product_count",
    y="product_category_name_english",
    palette="coolwarm",
    ax=axes[1],
)
axes[1].set_title("Bottom 5 Sold Products", fontsize=14)
st.pyplot(fig)

# Review Score
st.subheader("Review Score")
avg_review_score = review_score.mean()
most_common_review_score = review_score.value_counts().idxmax()

st.write(f"Average Review Score: **{avg_review_score:.2f}**")
st.write(f"Most Common Review Score: **{most_common_review_score}**")

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    x=review_score.index,
    y=review_score.values,
    palette="Blues",
    ax=ax,
)
ax.set_title("Review Score Distribution", fontsize=16)
ax.set_xlabel("Review Score", fontsize=14)
ax.set_ylabel("Frequency", fontsize=14)
st.pyplot(fig)

# Customer Demographic
st.subheader("Customer Demographic")
tab1, tab2 = st.tabs(["State", "Geolocation"])

with tab1:
    st.write(f"Most Common State: **{most_common_state}**")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(
        x=state.index,
        y=state.values,
        palette="viridis",
        ax=ax,
    )
    ax.set_title("Customers by State", fontsize=16)
    ax.set_xlabel("State", fontsize=14)
    ax.set_ylabel("Customer Count", fontsize=14)
    st.pyplot(fig)

with tab2:
    map_plot.plot()
