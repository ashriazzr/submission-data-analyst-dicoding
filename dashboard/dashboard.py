import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler

# Title of the dashboard
st.title("✨ Bike Sharing Insights: Weather & Seasonal Trends")

# Load the dataset from the provided URL
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

# URL for the external dataset
data_url = "https://raw.githubusercontent.com/ashriazzr/submission-data-analyst-dicoding/refs/heads/main/dashboard/all_data.csv"

# Load the dataset
data = load_data(data_url)

# Sidebar filters for weather and season
st.sidebar.header('🔍 Filter Data')

# Filter options for temperature and humidity
selected_temp = st.sidebar.selectbox('Select Temperature Range', ['All', 'Low', 'Medium', 'High'])
selected_humidity = st.sidebar.selectbox('Select Humidity Range', ['All', 'Low', 'Medium', 'High'])
selected_season = st.sidebar.selectbox('Select Season', data['season_day'].unique())

# Filter data by temperature
if selected_temp == 'Low':
    data = data[data['temp_hour'] < 0.3]
elif selected_temp == 'Medium':
    data = data[(data['temp_hour'] >= 0.3) & (data['temp_hour'] < 0.6)]
elif selected_temp == 'High':
    data = data[data['temp_hour'] >= 0.6]

# Filter data by humidity
if selected_humidity == 'Low':
    data = data[data['hum_hour'] < 50]
elif selected_humidity == 'Medium':
    data = data[(data['hum_hour'] >= 50) & (data['hum_hour'] < 70)]
elif selected_humidity == 'High':
    data = data[data['hum_hour'] >= 70]

# Filter data by season
data = data[data['season_day'] == selected_season]

# Check if filtered data is empty
if data.empty:
    st.warning("❌ No data available for the selected filters.")
else:
    # Question 1: Does Weather Affect Bike Rentals?
    st.header("☀️ Does Weather (Temperature & Humidity) Affect Bike Rentals?")
    
    # Create a scatter plot to show the relationship between temperature, humidity, and rentals
    fig, ax = plt.subplots()
    sns.scatterplot(data=data, x='temp_hour', y='hum_hour', hue='cnt_hour', 
                    palette='viridis', size='cnt_hour', sizes=(50, 200), 
                    ax=ax, edgecolor='black')
    ax.set_title("Temperature & Humidity vs Rentals", fontsize=14)
    ax.set_xlabel("Temperature (Normalized)", fontsize=12)
    ax.set_ylabel("Humidity (Normalized)", fontsize=12)
    st.pyplot(fig)

    # Display correlation between weather features and rentals
    st.subheader("📊 Correlation Between Weather and Rentals")
    correlation_data = data[['temp_hour', 'hum_hour', 'cnt_hour']]
    correlation_matrix = correlation_data.corr()

    # Display correlation matrix
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax2)
    ax2.set_title("Correlation Matrix", fontsize=14)
    st.pyplot(fig2)

    # Question 2: Seasonal Trends in Bike Rentals
    st.header("📈 Seasonal Trends in Bike Rentals")

    # Group data by season to analyze trends
    season_rentals = data.groupby('season_day')['cnt_hour'].mean()

    # Create an area plot to visualize the seasonal rental trends
    fig3, ax3 = plt.subplots()
    season_rentals.plot(kind='area', ax=ax3, color='skyblue', alpha=0.6, linewidth=3)
    ax3.set_title("Seasonal Bike Rental Trends", fontsize=14)
    ax3.set_xlabel("Season", fontsize=12)
    ax3.set_ylabel("Average Bike Rentals", fontsize=12)
    st.pyplot(fig3)

    # Display the average rentals by season
    avg_rentals = season_rentals.mean()
    st.markdown(f"<h3 style='font-size: 24px;'>Average Rentals for {selected_season} Season: {avg_rentals:.2f}</h3>", unsafe_allow_html=True)
