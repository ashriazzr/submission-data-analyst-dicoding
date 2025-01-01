import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Fungsi untuk memuat data dengan caching
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

# URL dataset utama
main_url = "https://raw.githubusercontent.com/hadarah1/public/main/bike_rental_hour.csv"
hour_url = "https://raw.githubusercontent.com/hadarah1/public/main/bike_rental_hour.csv"
day_url = "https://raw.githubusercontent.com/hadarah1/public/main/bike_rental_day.csv"

# Memuat dataset
main_data = load_data(main_url)
hour_data = load_data(hour_url)
day_data = load_data(day_url)

# Konversi kolom 'weathersit' dan 'season' menjadi kategori yang dapat dibaca
weather_mapping = {1: 'Clear', 2: 'Mist', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'}
season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}

main_data['weathersit'] = main_data['weathersit'].map(weather_mapping)
main_data['season'] = main_data['season'].map(season_mapping)

# Aplikasi Streamlit
st.title("Bike Rental Analysis Based on Weather and Season")

# Tampilkan dataset utama
st.header("Dataset Overview")
st.write("Preview of the dataset:")
st.write(main_data.head())

# Sidebar untuk filter
st.sidebar.header("Filter Options")
selected_weather = st.sidebar.multiselect(
    "Select Weather Conditions:", options=main_data['weathersit'].unique(), default=main_data['weathersit'].unique()
)
temp_range = st.sidebar.slider("Select Temperature Range:", float(main_data['temp'].min()), float(main_data['temp'].max()), (float(main_data['temp'].min()), float(main_data['temp'].max())))
hum_range = st.sidebar.slider("Select Humidity Range:", float(main_data['hum'].min()), float(main_data['hum'].max()), (float(main_data['hum'].min()), float(main_data['hum'].max())))

# Filter data berdasarkan input
filtered_data = main_data[
    (main_data['weathersit'].isin(selected_weather)) &
    (main_data['temp'].between(temp_range[0], temp_range[1])) &
    (main_data['hum'].between(hum_range[0], hum_range[1]))
]

# Visualisasi 1: Pengaruh Cuaca terhadap Penyewaan Sepeda
st.header("Effect of Weather on Bike Rentals")
st.write("Scatter plot of Temperature vs. Bike Rentals:")

fig1, ax1 = plt.subplots(figsize=(8, 6))
sns.scatterplot(
    data=filtered_data, x='temp', y='cnt', hue='weathersit', palette='Set2', ax=ax1
)
ax1.set_title("Temperature vs. Bike Rentals by Weather Condition")
ax1.set_xlabel("Temperature (Normalized)")
ax1.set_ylabel("Bike Rentals")
st.pyplot(fig1)

# Visualisasi 2: Tren Penyewaan Berdasarkan Musim
st.header("Bike Rentals by Season")
selected_season = st.sidebar.multiselect(
    "Select Seasons:", options=main_data['season'].unique(), default=main_data['season'].unique()
)
season_data = main_data[main_data['season'].isin(selected_season)]

st.write("Boxplot of Bike Rentals by Season:")
fig2, ax2 = plt.subplots(figsize=(8, 6))
sns.boxplot(data=season_data, x='season', y='cnt', palette='Set3', ax=ax2)
ax2.set_title("Distribution of Bike Rentals by Season")
ax2.set_xlabel("Season")
ax2.set_ylabel("Bike Rentals")
st.pyplot(fig2)

# Statistik Deskriptif Dataset Hour dan Day
st.header("Descriptive Statistics of Hourly and Daily Data")
if st.checkbox("Show Hourly Dataset Statistics"):
    st.write(hour_data.describe())
if st.checkbox("Show Daily Dataset Statistics"):
    st.write(day_data.describe())

# Insight Data
st.header("Key Insights")
st.write("1. Bike rentals tend to increase with temperature, but weather conditions also play a significant role.")
st.write("2. Rentals vary significantly by season, with Fall showing higher demand on average.")
st.write("3. Further analysis could explore the impact of holidays and working days on bike rentals.")
