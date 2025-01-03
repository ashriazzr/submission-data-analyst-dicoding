import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

st.title("✨ Bike Sharing Dashboard with Clustering🌞 ")

@st.cache_data
def load_data(url):
    """
    Function to load data from a given URL.
    Caches the data to optimize performance.
    """
    try:
        data = pd.read_csv(url)
        return data
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

main_data = load_data('https://raw.githubusercontent.com/ashriazzr/submission-data-analyst-dicoding/refs/heads/main/dashboard/all_data.csv')

if main_data.empty:
    st.error("Dataset is empty. Please check the URL or data source.")
else:
    st.success("Data loaded successfully!")

st.sidebar.header('🔍 Filter Options')

season_filter = st.sidebar.multiselect('Select Season', main_data['season'].unique(), main_data['season'].unique())
month_filter = st.sidebar.multiselect('Select Month', main_data['mnth'].unique(), main_data['mnth'].unique())

if st.sidebar.button("Reset Filters"):
    season_filter = main_data['season'].unique()
    month_filter = main_data['mnth'].unique()

filtered_data = main_data[(main_data['season'].isin(season_filter)) & (main_data['mnth'].isin(month_filter))]

if filtered_data.empty:
    st.warning("❌ No data available for the selected filters. Please select different options.")
else:
    st.header("Impact of Temperature and Humidity on Bike Rentals")
    summer_data = filtered_data[(filtered_data['mnth'] == 7) | (filtered_data['mnth'] == 8)]

    max_rentals = summer_data['cnt'].max()
    st.markdown(f"<h3 style='font-size: 24px;'>Max Rentals: {max_rentals}</h3>", unsafe_allow_html=True)

    fig, ax = plt.subplots()
    sns.scatterplot(data=summer_data, x='temp', y='cnt', ax=ax, color='orange', s=100, edgecolor='black')
    ax.set_title("Temperature vs Bike Rentals", fontsize=14)
    ax.set_xlabel("Temperature (Normalized)", fontsize=12)
    ax.set_ylabel("Number of Bike Rentals", fontsize=12)
    st.pyplot(fig)

    st.header("Monthly Bike Rental Trend")
    monthly_rentals = filtered_data.groupby('mnth')['cnt'].mean()

    fig2, ax2 = plt.subplots()
    monthly_rentals.plot(kind='line', ax=ax2, marker='o', color='blue', linewidth=2)
    ax2.set_title("Average Monthly Bike Rentals", fontsize=14)
    ax2.set_xlabel("Month", fontsize=12)
    ax2.set_ylabel("Average Bike Rentals", fontsize=12)
    st.pyplot(fig2)

    st.header("Bike Rentals by Working Days")
    total_weekend_rentals = filtered_data[filtered_data['workingday'] == 0]['cnt'].sum()
    total_weekday_rentals = filtered_data[filtered_data['workingday'] == 1]['cnt'].sum()

    st.markdown(f"<h3 style='font-size: 24px;'>Total Rentals on Weekends: {total_weekend_rentals}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='font-size: 24px;'>Total Rentals on Working Days: {total_weekday_rentals}</h3>", unsafe_allow_html=True)

    fig3, ax3 = plt.subplots()
    sns.barplot(x=['Weekend', 'Working Day'], y=[total_weekend_rentals, total_weekday_rentals], ax=ax3, palette="pastel")
    ax3.set_title("Bike Rentals on Working Days vs Weekends", fontsize=14)
    ax3.set_xlabel("Day Type", fontsize=12)
    ax3.set_ylabel("Number of Rentals", fontsize=12)
    st.pyplot(fig3)

    st.header("🌧️ Average Bike Rentals by Temperature and Humidity")
    filtered_data['temp_group'] = pd.cut(filtered_data['temp'], bins=3, labels=['Low', 'Medium', 'High'])
    filtered_data['hum_group'] = pd.cut(filtered_data['hum'], bins=3, labels=['Low', 'Medium', 'High'])
    avg_rental_by_temp_hum = filtered_data.groupby(['temp_group', 'hum_group'], observed=True)['cnt'].mean().unstack()

    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.heatmap(avg_rental_by_temp_hum, annot=True, cmap='coolwarm', fmt=".2f", ax=ax4)
    ax4.set_title('Average Bike Rentals Based on Temperature and Humidity', fontsize=14)
    ax4.set_xlabel('Humidity Group', fontsize=12)
    ax4.set_ylabel('Temperature Group', fontsize=12)
    st.pyplot(fig4)

    st.header("📊 Clustering: Grouping Bike Rentals by Features")

    cluster_data = filtered_data[['temp', 'hum', 'cnt']].dropna()
    scaler = StandardScaler()
    scaled_cluster_data = scaler.fit_transform(cluster_data)

    kmeans = KMeans(n_clusters=3, random_state=42)
    cluster_labels = kmeans.fit_predict(scaled_cluster_data)
    filtered_data['Cluster'] = cluster_labels

    fig5, ax5 = plt.subplots()
    sns.scatterplot(data=filtered_data, x='temp', y='hum', hue='Cluster', palette='Set1', s=100, edgecolor='black', ax=ax5)
    ax5.set_title("Clusters of Bike Rentals Based on Features", fontsize=14)
    ax5.set_xlabel("Temperature (Normalized)", fontsize=12)
    ax5.set_ylabel("Humidity (Normalized)", fontsize=12)
    st.pyplot(fig5)

    st.markdown("### Cluster Centers")
    cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
    cluster_centers_df = pd.DataFrame(cluster_centers, columns=['Temperature', 'Humidity', 'Rentals'])
    st.dataframe(cluster_centers_df)
