import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("✨ Bike Sharing Insights: Weather & Seasonal Trends")

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

data_url = "https://raw.githubusercontent.com/ashriazzr/submission-data-analyst-dicoding/refs/heads/main/dashboard/all_data.csv"

data = load_data(data_url)
st.sidebar.header('🔍 Filter Data')

selected_weather = st.sidebar.multiselect('Select Weather Conditions (Temperature & Humidity)', ['Low Temp', 'Medium Temp', 'High Temp', 'Low Humidity', 'Medium Humidity', 'High Humidity'], ['Low Temp', 'Medium Temp', 'High Temp', 'Low Humidity', 'Medium Humidity', 'High Humidity'])
selected_season = st.sidebar.selectbox('Select Season', data['season'].unique())

if 'Low Temp' in selected_weather:
    weather_temp_filter = data[data['temp'] < 0.3]
elif 'Medium Temp' in selected_weather:
    weather_temp_filter = data[(data['temp'] >= 0.3) & (data['temp'] < 0.6)]
elif 'High Temp' in selected_weather:
    weather_temp_filter = data[data['temp'] >= 0.6]
else:
    weather_temp_filter = data

if 'Low Humidity' in selected_weather:
    weather_hum_filter = weather_temp_filter[weather_temp_filter['hum'] < 50]
elif 'Medium Humidity' in selected_weather:
    weather_hum_filter = weather_temp_filter[(weather_temp_filter['hum'] >= 50) & (weather_temp_filter['hum'] < 70)]
elif 'High Humidity' in selected_weather:
    weather_hum_filter = weather_temp_filter[weather_temp_filter['hum'] >= 70]
else:
    weather_hum_filter = weather_temp_filter

# Filter data by season
season_data = weather_hum_filter[weather_hum_filter['season'] == selected_season]

if season_data.empty:
    st.warning("❌ No data available for the selected filters.")
else:

    st.header("☀️ Does Weather (Temperature & Humidity) Affect Bike Rentals?")
    
    fig, ax = plt.subplots()
    sns.scatterplot(data=season_data, x='temp', y='hum', hue='cnt', palette='viridis', size='cnt', sizes=(50, 200), ax=ax, edgecolor='black')
    ax.set_title("Temperature & Humidity vs Rentals", fontsize=14)
    ax.set_xlabel("Temperature (Normalized)", fontsize=12)
    ax.set_ylabel("Humidity (Normalized)", fontsize=12)
    st.pyplot(fig)

    st.subheader("📊 Correlation Between Weather and Rentals")
    correlation_data = season_data[['temp', 'hum', 'cnt']]
    correlation_matrix = correlation_data.corr()

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax2)
    ax2.set_title("Correlation Matrix", fontsize=14)
    st.pyplot(fig2)

    # Question 2: Seasonal Trends in Bike Rentals
    st.header("📈 Seasonal Trends in Bike Rentals")

    season_rentals = season_data.groupby('season')['cnt'].mean()

    fig3, ax3 = plt.subplots()
    season_rentals.plot(kind='area', ax=ax3, color='skyblue', alpha=0.6, linewidth=3)
    ax3.set_title("Seasonal Bike Rental Trends", fontsize=14)
    ax3.set_xlabel("Season", fontsize=12)
    ax3.set_ylabel("Average Bike Rentals", fontsize=12)
    st.pyplot(fig3)

    st.markdown(f"<h3 style='font-size: 24px;'>Average Rentals for {selected_season} Season: {season_rentals.mean():.2f}</h3>", unsafe_allow_html=True)
