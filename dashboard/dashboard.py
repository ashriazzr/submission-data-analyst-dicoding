import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul aplikasi
st.title("Analisis Penyewaan Sepeda berdasarkan Data Cuaca dan Musim")

# URL file CSV di GitHub
url = "https://raw.githubusercontent.com/ashriazzr/submission-data-analyst-dicoding/refs/heads/main/dashboard/all_data.csv"

# Membaca CSV dari URL
df = pd.read_csv(url)

# Menampilkan data secara keseluruhan
st.subheader("Data Penyewaan Sepeda")
st.write(df)

# Konversi kolom 'dteday' ke format datetime jika tersedia
if 'dteday' in df.columns:
    df['dteday'] = pd.to_datetime(df['dteday'], errors='coerce')

# Pertanyaan 1: Apakah Cuaca (Weather, Temperature, Humidity) Memengaruhi Jumlah Penyewaan Sepeda?
st.subheader("1. Pengaruh Cuaca terhadap Penyewaan Sepeda")

# Fitur filter untuk cuaca (weathersit) dan rentang suhu/humidity
st.sidebar.header("Filter untuk Visualisasi Cuaca")
weathersit_options = df['weathersit'].unique()
selected_weather = st.sidebar.multiselect("Pilih jenis cuaca:", weathersit_options, default=weathersit_options)

temp_range = st.sidebar.slider("Pilih rentang suhu (°C):", 
                                float(df['temp'].min()), 
                                float(df['temp'].max()), 
                                (float(df['temp'].min()), float(df['temp'].max())))

humidity_range = st.sidebar.slider("Pilih rentang kelembapan (%):", 
                                    float(df['hum'].min()), 
                                    float(df['hum'].max()), 
                                    (float(df['hum'].min()), float(df['hum'].max())))

# Filter data berdasarkan pilihan
filtered_df_1 = df[(df['weathersit'].isin(selected_weather)) &
                   (df['temp'] >= temp_range[0]) & (df['temp'] <= temp_range[1]) &
                   (df['hum'] >= humidity_range[0]) & (df['hum'] <= humidity_range[1])]

# Visualisasi scatter plot
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=filtered_df_1, x='temp', y='cnt', hue='weathersit', palette='coolwarm', ax=ax)
ax.set_title("Hubungan antara Suhu dan Jumlah Penyewaan Sepeda berdasarkan Cuaca", fontsize=16)
ax.set_xlabel('Suhu (°C)', fontsize=14)
ax.set_ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
st.pyplot(fig)

# Pertanyaan 2: Bagaimana Tren Penyewaan Sepeda Berdasarkan Musim?
st.subheader("2. Tren Penyewaan Sepeda Berdasarkan Musim")

# Fitur filter untuk musim (season)
st.sidebar.header("Filter untuk Visualisasi Musim")
season_options = df['season'].unique()
selected_seasons = st.sidebar.multiselect("Pilih musim:", season_options, default=season_options)

# Filter data berdasarkan pilihan musim
filtered_df_2 = df[df['season'].isin(selected_seasons)]

# Visualisasi boxplot berdasarkan musim
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=filtered_df_2, x='season', y='cnt', palette='Set2', ax=ax)
ax.set_title("Tren Penyewaan Sepeda Berdasarkan Musim", fontsize=16)
ax.set_xlabel('Musim', fontsize=14)
ax.set_ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
st.pyplot(fig)
