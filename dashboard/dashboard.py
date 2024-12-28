import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style="darkgrid")

# URL Dataset
all_data_url = "https://github.com/ashriazzr/submission-data-analyst-dicoding/blob/main/dashboard/all_data.csv"
all_geo_url = "https://raw.githubusercontent.com/ashriazzr/submission-data-analyst-dicoding/main/dashboard/geo_.csv"

# Fungsi untuk memuat data
@st.cache_data
def load_data(url):
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Load datasets
all_df = load_data(all_data_url)
geolocation = load_data(all_geo_url)

if all_df.empty or geolocation.empty:
    st.stop()

# Preprocessing
datetime_cols = [
    "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date",
    "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"
]

for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col], errors="coerce")

all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(drop=True, inplace=True)

geolocation_unique = geolocation.drop_duplicates(subset="customer_unique_id")

# Filter Date Range
min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

with st.sidebar:
    st.markdown("## Filter by Date Range")
    start_date, end_date = st.date_input(
        "Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# Validasi tanggal
if start_date > end_date:
    st.error("Start date cannot be greater than end date.")
    st.stop()

# Filter Data
main_df = all_df[
    (all_df["order_approved_at"] >= pd.Timestamp(start_date)) &
    (all_df["order_approved_at"] <= pd.Timestamp(end_date))
]

# Fungsi analisis
@st.cache_data
def create_daily_orders_df(df):
    return df.groupby(df["order_approved_at"].dt.date).size().reset_index(name="order_count")

@st.cache_data
def create_sum_spend_df(df):
    return df.groupby(df["order_approved_at"].dt.date)["payment_value"].sum().reset_index(name="total_spend")

@st.cache_data
def create_sum_order_items_df(df):
    return df.groupby("product_category_name_english").size().reset_index(name="product_count")

@st.cache_data
def review_score_analysis(df):
    return df["review_score"].value_counts().sort_index()

@st.cache_data
def customer_state_analysis(df):
    return df["customer_state"].value_counts()

# Analisis dan Visualisasi
st.title("E-Commerce Public Data Analysis")

# Daily Orders Analysis
st.subheader("Daily Orders Delivered")
daily_orders_df = create_daily_orders_df(main_df)
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=daily_orders_df, x="order_approved_at", y="order_count", marker="o", ax=ax)
ax.set_title("Daily Orders Delivered Over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Number of Orders")
plt.xticks(rotation=45)
st.pyplot(fig)

# Customer Spend Analysis
st.subheader("Customer Spending Over Time")
sum_spend_df = create_sum_spend_df(main_df)
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=sum_spend_df, x="order_approved_at", y="total_spend", marker="o", ax=ax)
ax.set_title("Total Spending by Customers")
ax.set_xlabel("Date")
ax.set_ylabel("Total Spending (Currency)")
plt.xticks(rotation=45)
st.pyplot(fig)

# Top Product Categories
st.subheader("Top Product Categories")
sum_order_items_df = create_sum_order_items_df(main_df)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    data=sum_order_items_df.sort_values(by="product_count", ascending=False).head(5),
    x="product_count",
    y="product_category_name_english",
    palette="viridis",
    ax=ax
)
ax.set_title("Top 5 Most Sold Product Categories")
ax.set_xlabel("Number of Products Sold")
ax.set_ylabel("Product Category")
st.pyplot(fig)

# Review Score Distribution
st.subheader("Review Score Distribution")
review_scores = review_score_analysis(main_df)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=review_scores.index, y=review_scores.values, palette="viridis", ax=ax)
ax.set_title("Distribution of Customer Review Scores")
ax.set_xlabel("Review Score")
ax.set_ylabel("Number of Reviews")
st.pyplot(fig)

# Customer Demographics by State
st.subheader("Customer Demographics by State")
state_analysis = customer_state_analysis(main_df)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=state_analysis.index, y=state_analysis.values, palette="viridis", ax=ax)
ax.set_title("Customer Distribution by State")
ax.set_xlabel("State")
ax.set_ylabel("Number of Customers")
plt.xticks(rotation=45)
st.pyplot(fig)

st.markdown("---")
st.markdown("Data visualization and insights generated using Streamlit.")
