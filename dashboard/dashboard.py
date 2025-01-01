import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul aplikasi
st.title("Aplikasi Streamlit untuk Analisis Penyewaan Sepeda")

# URL file CSV di GitHub
url = "https://raw.githubusercontent.com/ashriazzr/submission-data-analyst-dicoding/refs/heads/main/dashboard/all_data.csv"

try:
    # Membaca CSV dari URL
    df = pd.read_csv(url)
    df['dteday'] = pd.to_datetime(df['dteday'], errors='coerce')  # Format kolom tanggal

    # Validasi kolom yang diperlukan
    required_columns = {'temp', 'cnt', 'weathersit', 'season', 'dteday'}
    if not required_columns.issubset(df.columns):
        st.error("Dataset tidak memiliki kolom yang diperlukan untuk analisis.")
        st.stop()

    # Fitur filter untuk visualisasi
    st.sidebar.header("Filter Data Visualisasi")

    # Filter berdasarkan rentang tanggal
    start_date, end_date = st.sidebar.date_input(
        "Pilih rentang tanggal",
        [df['dteday'].min(), df['dteday'].max()]
    )
    df = df[(df['dteday'] >= pd.to_datetime(start_date)) & 
            (df['dteday'] <= pd.to_datetime(end_date))]

    # Filter berdasarkan cuaca
    weather_options = df['weathersit'].unique()
    selected_weather = st.sidebar.multiselect("Pilih Cuaca (Weather)", options=weather_options, default=weather_options)
    df = df[df['weathersit'].isin(selected_weather)]

    # Filter berdasarkan musim
    season_options = df['season'].unique()
    selected_season = st.sidebar.multiselect("Pilih Musim (Season)", options=season_options, default=season_options)
    df = df[df['season'].isin(selected_season)]

    # Periksa apakah dataset kosong setelah filter
    if df.empty:
        st.warning("Dataset kosong setelah penerapan filter. Harap ubah filter Anda.")
        st.stop()

    # Menjawab Pertanyaan 1: Pengaruh Cuaca terhadap Penyewaan Sepeda
    st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.scatterplot(x=df['temp'], y=df['cnt'], hue=df['weathersit'], palette='coolwarm', s=50, alpha=0.7, ax=ax)
    ax.set_title("Hubungan antara Suhu dan Jumlah Penyewaan Sepeda berdasarkan Cuaca", fontsize=18)
    ax.set_xlabel('Suhu (°C)', fontsize=14)
    ax.set_ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
    ax.legend(title='Cuaca', fontsize=12)
    st.pyplot(fig)

    # Menjawab Pertanyaan 2: Tren Penyewaan Sepeda Berdasarkan Musim
    st.subheader("Tren Penyewaan Sepeda Berdasarkan Musim")

    fig, ax = plt.subplots(figsize=(12, 8))
    sns.boxplot(x=df['season'], y=df['cnt'], palette='Set2', ax=ax)
    ax.set_title("Tren Penyewaan Sepeda Berdasarkan Musim", fontsize=18)
    ax.set_xlabel('Musim', fontsize=14)
    ax.set_ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
    ax.set_xticklabels(['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'], fontsize=12)
    st.pyplot(fig)

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
