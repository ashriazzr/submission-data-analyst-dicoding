import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul aplikasi
st.title("Aplikasi Streamlit untuk Analisis Penyewaan Sepeda")

# URL file CSV di GitHub
url = "https://raw.githubusercontent.com/ashriazzr/submission-data-analyst-dicoding/refs/heads/main/dashboard/all_data.csv"

# Membaca CSV dari URL
df = pd.read_csv(url)
df['dteday'] = pd.to_datetime(df['dteday'], errors='coerce')  # Pastikan kolom tanggal diformat dengan benar

# Menambahkan kolom untuk Tahun, Bulan, dan Hari
df['year'] = df['dteday'].dt.year
df['month'] = df['dteday'].dt.month
df['day'] = df['dteday'].dt.day

# Fitur filter untuk visualisasi
st.sidebar.header("Filter Data Visualisasi")

# Filter berdasarkan rentang tanggal
start_date, end_date = st.sidebar.date_input("Pilih rentang tanggal", 
                                              [df['dteday'].min(), df['dteday'].max()])
df = df[(df['dteday'] >= pd.to_datetime(start_date)) & 
        (df['dteday'] <= pd.to_datetime(end_date))]

# Filter berdasarkan tahun
years = df['year'].unique()
selected_years = st.sidebar.multiselect("Pilih Tahun", options=years, default=years)
df = df[df['year'].isin(selected_years)]

# Filter berdasarkan bulan
months = range(1, 13)
selected_months = st.sidebar.multiselect("Pilih Bulan", options=months, default=months)
df = df[df['month'].isin(selected_months)]

# Filter berdasarkan hari
days = range(1, 32)
selected_days = st.sidebar.multiselect("Pilih Hari", options=days, default=days)
df = df[df['day'].isin(selected_days)]

# Filter berdasarkan cuaca
weather_options = df['weathersit'].unique()
selected_weather = st.sidebar.multiselect("Pilih Cuaca (Weather)", options=weather_options, default=weather_options)
df = df[df['weathersit'].isin(selected_weather)]

# Filter berdasarkan musim
season_options = df['season'].unique()
selected_season = st.sidebar.multiselect("Pilih Musim (Season)", options=season_options, default=season_options)
df = df[df['season'].isin(selected_season)]

# Menjawab Pertanyaan 1: Apakah Cuaca (Weather, Temperature, Humidity) Memengaruhi Jumlah Penyewaan Sepeda?
st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")

fig, ax = plt.subplots(figsize=(12, 8))
sns.scatterplot(x=df['temp'], y=df['cnt'], hue=df['weathersit'], palette='coolwarm', s=50, alpha=0.7, ax=ax)
ax.set_title("Hubungan antara Suhu dan Jumlah Penyewaan Sepeda berdasarkan Cuaca", fontsize=18)
ax.set_xlabel('Suhu (°C)', fontsize=14)
ax.set_ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
ax.legend(title='Cuaca', fontsize=12)
st.pyplot(fig)

# Menjawab Pertanyaan 2: Bagaimana Tren Penyewaan Sepeda Berdasarkan Musim?
st.subheader("Tren Penyewaan Sepeda Berdasarkan Musim")

fig, ax = plt.subplots(figsize=(12, 8))
sns.boxplot(x=df['season'], y=df['cnt'], palette='Set2', ax=ax)
ax.set_title("Tren Penyewaan Sepeda Berdasarkan Musim", fontsize=18)
ax.set_xlabel('Musim', fontsize=14)
ax.set_ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
ax.set_xticklabels(['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'], fontsize=12)
st.pyplot(fig)
