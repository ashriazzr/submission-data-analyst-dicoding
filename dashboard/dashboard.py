import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib
from func import DataAnalyzer, BrazilMapPlotter

sns.set(style='dark')
st.set_option('deprecation.showPyplotGlobalUse', False)

datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
datetime_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", 
                 "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]

# Load datasets
all_df = pd.read_csv("https://github.com/ashriazzr/submission-data-analyst-dicoding/tree/main/dasboard/df.csv")
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)
all_df.reset_index(drop=True, inplace=True)

# Geolocation Dataset
geolocation = pd.read_csv('https://github.com/ashriazzr/submission-data-analyst-dicoding/tree/main/dasboard/geolocation.csv')
data = geolocation.drop_duplicates(subset='customer_unique_id')

# Convert columns to datetime
for col in datetime_cols:
    all_df[col] = pd.to_datetime(all_df[col])

@@ -30,8 +32,7 @@
    with col1:
        st.write(' ')
    with col2:
        
        st.write(' ')

@@ -43,10 +44,11 @@
        max_value=max_date
    )

# Main
main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                 (all_df["order_approved_at"] <= str(end_date))]
# Filter data based on selected date range
main_df = all_df[(all_df["order_approved_at"] >= pd.Timestamp(start_date)) & 
                 (all_df["order_approved_at"] <= pd.Timestamp(end_date))]

# Analyze data
function = DataAnalyzer(main_df)
map_plot = BrazilMapPlotter(data, plt, mpimg, urllib, st)

@@ -57,14 +59,11 @@
state, most_common_state = function.create_bystate_df()
order_status, common_status = function.create_order_status()

# Define your Streamlit app
st.title("E-Commerce Public Data Analysist")

# Add text or descriptions
st.write("**Dashboard for Analyzing E-Commerce Public Data.**")
# Streamlit app
st.title("E-Commerce Public Data Analysis")

# Daily Orders Delivered
st.subheader("Daily Orders Deliver")
st.subheader("Daily Orders Delivered")
col1, col2 = st.columns(2)

with col1:
@@ -108,7 +107,6 @@
    linewidth=2,
    color="#90CAF9"
)

ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)
@@ -125,25 +123,24 @@
    avg_items = sum_order_items_df["product_count"].mean()
    st.markdown(f"Average Items: **{avg_items}**")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(45, 25))

sns.barplot(x="product_count", y="product_category_name_english", data=sum_order_items_df.head(5), palette="viridis", ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=80)
ax[0].set_title("Most sold products", loc="center", fontsize=90)
ax[0].tick_params(axis ='y', labelsize=55)
ax[0].tick_params(axis ='x', labelsize=50)

sns.barplot(x="product_count", y="product_category_name_english", data=sum_order_items_df.sort_values(by="product_count", ascending=True).head(5), palette="viridis", ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=80)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Fewest products sold", loc="center", fontsize=90)
ax[1].tick_params(axis='y', labelsize=55)
ax[1].tick_params(axis='x', labelsize=50)
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
@@ -159,45 +156,32 @@
    st.markdown(f"Most Common Review Score: **{most_common_review_score}**")

fig, ax = plt.subplots(figsize=(12, 6))
colors = sns.color_palette("viridis", len(review_score))

sns.barplot(x=review_score.index,
            y=review_score.values,
            order=review_score.index,
            palette=colors)

plt.title("Customer Review Scores for Service", fontsize=15)
plt.xlabel("Rating")
plt.ylabel("Count")
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

for i, v in enumerate(review_score.values):
    ax.text(i, v + 5, str(v), ha='center', va='bottom', fontsize=12, color='black')

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
    most_common_state = state.customer_state.value_counts().index[0]
    most_common_state = state.customer_state.value_counts().idxmax()
    st.markdown(f"Most Common State: **{most_common_state}**")

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=state.customer_state.value_counts().index,
                y=state.customer_count.values, 
                data=state,
                palette="viridis"
                    )

    plt.title("Number customers from State", fontsize=15)
    plt.xlabel("State")
    plt.ylabel("Number of Customers")
    plt.xticks(fontsize=12)
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


Footer
© 2024 Gi
