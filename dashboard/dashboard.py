import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="dark")

datetime_cols = [
    "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date",
    "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"
]

# Load datasets
all_df_url = "https://raw.githubusercontent.com/ashriazzr/submission-data-analyst-dicoding/refs/heads/main/dashboard/df.csv"
geolocation_url = "https://raw.githubusercontent.com/ashriazzr/submission-data-analyst-dicoding/refs/heads/main/dashboard/geolocation.csv"

all_df = pd.read_csv(all_df_url)
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(drop=True, inplace=True)

geolocation = pd.read_csv(geolocation_url)
unique_geolocation = geolocation.drop_duplicates(subset="customer_unique_id")

# Convert columns to datetime
for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

# Sidebar for date range
with st.sidebar:
    st.markdown("## Filter by Date Range")
    start_date, end_date = st.date_input(
        "Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Filter data based on date range
main_df = all_df[(all_df["order_approved_at"] >= pd.Timestamp(start_date)) &
                 (all_df["order_approved_at"] <= pd.Timestamp(end_date))]

# Placeholder functions for analysis
# Replace these with actual implementations
@st.cache
def create_daily_orders_df(df):
    return df.groupby("order_approved_at").size().reset_index(name="order_count")

def create_sum_spend_df(df):
    return df.groupby("order_approved_at")["payment_value"].sum().reset_index(name="total_spend")

def create_sum_order_items_df(df):
    return df.groupby("product_category_name_english").size().reset_index(name="product_count")

def review_score_analysis(df):
    return df["review_score"].value_counts()

def customer_state_analysis(df):
    return df["customer_state"].value_counts()

# Data Analysis
st.title("E-Commerce Public Data Analysis")

# Daily Orders Analysis
daily_orders_df = create_daily_orders_df(main_df)
st.subheader("Daily Orders Delivered")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=daily_orders_df, x="order_approved_at", y="order_count", marker="o", ax=ax)
ax.set_title("Daily Orders Delivered")
ax.tick_params(axis="x", rotation=45)
st.pyplot(fig)

# Customer Spend Analysis
sum_spend_df = create_sum_spend_df(main_df)
st.subheader("Customer Spend Analysis")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=sum_spend_df, x="order_approved_at", y="total_spend", marker="o", ax=ax)
ax.set_title("Customer Spending Over Time")
ax.tick_params(axis="x", rotation=45)
st.pyplot(fig)

# Order Items Analysis
sum_order_items_df = create_sum_order_items_df(main_df)
st.subheader("Top Product Categories")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=sum_order_items_df.head(5), x="product_count", y="product_category_name_english", palette="viridis", ax=ax)
ax.set_title("Most Sold Product Categories")
st.pyplot(fig)

# Review Score Analysis
review_scores = review_score_analysis(main_df)
st.subheader("Review Score Distribution")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=review_scores.index, y=review_scores.values, palette="viridis", ax=ax)
ax.set_title("Customer Review Scores")
st.pyplot(fig)

# Customer Demographics Analysis
state_analysis = customer_state_analysis(main_df)
st.subheader("Customer Demographics by State")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=state_analysis.index, y=state_analysis.values, palette="viridis", ax=ax)
ax.set_title("Customer Distribution by State")
ax.tick_params(axis="x", rotation=45)
st.pyplot(fig)

st.markdown("---")
st.markdown("Data visualization and insights generated using Streamlit.")
