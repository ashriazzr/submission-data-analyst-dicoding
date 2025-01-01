
# URL dataset utama
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Title of the dashboard
st.title("✨ Bike Sharing Insights with Clustering")

# Load the dataset using caching for better performance
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Load the dataset
data = "https://raw.githubusercontent.com/ashriazzr/submission-data-analyst-dicoding/refs/heads/main/dashboard/all_data.csv"

# Sidebar filters
st.sidebar.header('🔍 Filter Data')

# Filter options for season and month
selected_seasons = st.sidebar.multiselect('Select Season Day', data['season_day'].unique(), data['season_day'].unique())
selected_months = st.sidebar.multiselect('Select Month Hour', data['mnth_hour'].unique(), data['mnth_hour'].unique())

# Button to reset filters
if st.sidebar.button("Reset Filters"):
    selected_seasons = data['season_day'].unique()
    selected_months = data['mnth_hour'].unique()

# Filter data based on user input
filtered_data = data[(data['season_day'].isin(selected_seasons)) & (data['mnth_hour'].isin(selected_months))]

# Check if filtered data is empty
if filtered_data.empty:
    st.warning("❌ No data matches the selected criteria. Try different options.")
else:
    # Analyzing the effect of temperature and humidity on rentals during summer
    st.header("🌞 Temperature & Humidity Impact on Summer Rentals")
    summer_data = filtered_data[(filtered_data['mnth_hour'] == 7) | (filtered_data['mnth_hour'] == 8)]

    # Display maximum rentals during the summer
    max_summer_rentals = summer_data['cnt_hour'].max()
    st.markdown(f"<h3 style='font-size: 24px;'>Max Rentals in Summer: {max_summer_rentals}</h3>", unsafe_allow_html=True)

    # Improved visualization: Violin plot of temperature vs bike rentals to show distribution
    fig, ax = plt.subplots()
    sns.violinplot(x='temp_hour', y='cnt_hour', data=summer_data, ax=ax, palette='Oranges', scale='count')
    ax.set_title("Distribution of Rentals vs Temperature in Summer", fontsize=14)
    ax.set_xlabel("Temperature (Normalized)", fontsize=12)
    ax.set_ylabel("Number of Rentals", fontsize=12)
    st.pyplot(fig)

    # Monthly rental trends with improved visualization: Area plot for trend representation
    st.header("📈 Monthly Rental Trends (January to December)")
    monthly_avg_rentals = filtered_data.groupby('mnth_hour')['cnt_hour'].mean()

    # Display average rentals for selected months
    selected_month_avg_rentals = monthly_avg_rentals.mean()
    st.markdown(f"<h3 style='font-size: 24px;'>Average Rentals for Selected Months: {selected_month_avg_rentals:.2f}</h3>", unsafe_allow_html=True)

    # Area chart for monthly rental trends
    fig2, ax2 = plt.subplots()
    monthly_avg_rentals.plot(kind='area', ax=ax2, color='skyblue', alpha=0.4, linewidth=3)
    ax2.set_title("Monthly Average Bike Rentals", fontsize=14)
    ax2.set_xlabel("Month", fontsize=12)
    ax2.set_ylabel("Average Rentals", fontsize=12)
    st.pyplot(fig2)

    # Rental trends based on weekdays and weather conditions using a more advanced stacked bar plot
    st.header("☀️ Rentals by Weather and Workdays")
    weekend_rentals = filtered_data[filtered_data['workingday_hour'] == 0]['cnt_hour'].sum()
    weekday_rentals = filtered_data[filtered_data['workingday_hour'] == 1]['cnt_hour'].sum()
    st.markdown(f"<h3 style='font-size: 24px;'>Weekend Rentals: {weekend_rentals}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='font-size: 24px;'>Weekday Rentals: {weekday_rentals}</h3>", unsafe_allow_html=True)

    # Stacked bar chart for rentals
    fig3, ax3 = plt.subplots()
    sns.barplot(x=['Weekend', 'Weekday'], y=[weekend_rentals, weekday_rentals], ax=ax3, palette="coolwarm", dodge=False)
    ax3.set_title("Bike Rentals on Weekdays vs Weekends", fontsize=14)
    ax3.set_xlabel("Day Type", fontsize=12)
    ax3.set_ylabel("Number of Rentals", fontsize=12)
    st.pyplot(fig3)

    # Heatmap of average rentals by temperature and humidity with an improved color scheme
    st.header("🌧️ Average Rentals by Temperature & Humidity")
    filtered_data['temp_category'] = pd.cut(filtered_data['temp_hour'], bins=3, labels=['Low', 'Medium', 'High'])
    filtered_data['hum_category'] = pd.cut(filtered_data['hum_hour'], bins=3, labels=['Low', 'Medium', 'High'])
    rentals_by_temp_hum = filtered_data.groupby(['temp_category', 'hum_category'], observed=True)['cnt_hour'].mean().unstack()

    # Display max rentals based on temperature and humidity categories
    max_avg_rentals_temp_hum = rentals_by_temp_hum.stack().max()
    st.markdown(f"<h3 style='font-size: 24px;'>Max Average Rentals by Temp & Humidity: {max_avg_rentals_temp_hum:.2f}</h3>", unsafe_allow_html=True)

    # Heatmap with a refined color palette
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.heatmap(rentals_by_temp_hum, annot=True, cmap='YlGnBu', fmt=".2f", ax=ax4, linewidths=1)
    ax4.set_title('Average Rentals by Temperature and Humidity', fontsize=14)
    ax4.set_xlabel('Humidity Category', fontsize=12)
    ax4.set_ylabel('Temperature Category', fontsize=12)
    st.pyplot(fig4)

    # K-means clustering with a unique visualization: Pairplot
    st.header("📊 Clustering: Grouping Rentals by Temp & Humidity")

    # Selecting features for clustering
    cluster_data = filtered_data[['temp_hour', 'hum_hour', 'cnt_hour']].dropna()

    # Normalize the data before clustering
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(cluster_data)

    # Perform clustering with K-means (3 clusters)
    kmeans = KMeans(n_clusters=3, random_state=42)
    cluster_labels = kmeans.fit_predict(scaled_data)

    # Add cluster labels to data
    filtered_data['Cluster'] = cluster_labels

    # Visualize clustering using pairplot
    fig5 = sns.pairplot(filtered_data, hue='Cluster', palette='Set2', vars=['temp_hour', 'hum_hour', 'cnt_hour'], height=3)
    st.pyplot(fig5)

    # Display cluster centers
    st.markdown("### Cluster Centers")
    cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
    cluster_centers_df = pd.DataFrame(cluster_centers, columns=['Temperature', 'Humidity', 'Rentals'])
    st.dataframe(cluster_centers_df)

