import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul aplikasi
st.title("Aplikasi Streamlit untuk Mengelola Data Penyewaan Sepeda")

# URL file CSV di GitHub
url = "https://raw.githubusercontent.com/ashriazzr/submission-data-analyst-dicoding/refs/heads/main/dashboard/all_data.csv"

# Membaca CSV dari URL
df = pd.read_csv(url)

# Menampilkan data
st.subheader("Data yang Diupload")
st.write(df)

# Pertanyaan 1: Apakah cuaca (weather, temperature, humidity) memengaruhi jumlah penyewaan sepeda?
st.subheader("Apakah cuaca (weather, temperature, humidity) memengaruhi jumlah penyewaan sepeda?")
weather_columns = ['weather', 'temperature', 'humidity', 'count']  # Kolom yang relevan
if all(col in df.columns for col in weather_columns):
    # Visualisasi hubungan antara cuaca, suhu, kelembaban, dan jumlah penyewaan sepeda
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))

    # Visualisasi suhu terhadap jumlah penyewaan sepeda
    sns.scatterplot(x=df['temperature'], y=df['count'], ax=ax[0], color='b')
    ax[0].set_title("Suhu vs Penyewaan Sepeda")
    ax[0].set_xlabel("Suhu (°C)")
    ax[0].set_ylabel("Jumlah Penyewaan Sepeda")

    # Visualisasi kelembaban terhadap jumlah penyewaan sepeda
    sns.scatterplot(x=df['humidity'], y=df['count'], ax=ax[1], color='g')
    ax[1].set_title("Kelembaban vs Penyewaan Sepeda")
    ax[1].set_xlabel("Kelembaban (%)")
    ax[1].set_ylabel("Jumlah Penyewaan Sepeda")

    # Visualisasi cuaca terhadap jumlah penyewaan sepeda
    sns.boxplot(x=df['weather'], y=df['count'], ax=ax[2], color='r')
    ax[2].set_title("Cuaca vs Penyewaan Sepeda")
    ax[2].set_xlabel("Cuaca")
    ax[2].set_ylabel("Jumlah Penyewaan Sepeda")

    st.pyplot(fig)
else:
    st.write("Data cuaca atau penyewaan sepeda tidak lengkap.")

# Pertanyaan 2: Bagaimana tren penyewaan sepeda berdasarkan musim (season)?
st.subheader("Bagaimana tren penyewaan sepeda berdasarkan musim?")
if 'season' in df.columns and 'count' in df.columns:
    # Visualisasi tren penyewaan sepeda berdasarkan musim
    plt.figure(figsize=(8, 5))
    sns.boxplot(x=df['season'], y=df['count'], palette='Set2')
    plt.title("Tren Penyewaan Sepeda Berdasarkan Musim")
    plt.xlabel("Musim")
    plt.ylabel("Jumlah Penyewaan Sepeda")
    st.pyplot(plt)
else:
    st.write("Data musim atau penyewaan sepeda tidak lengkap.")

# Menyediakan tombol untuk mendownload data yang terfilter
if st.button('Download Data yang Terfilter'):
    filtered_file = df.to_csv(index=False)
    st.download_button(label="Download CSV", data=filtered_file, file_name="filtered_data.csv", mime="text/csv")

# Menyediakan tombol untuk mendownload data asli
if st.button('Download Data Asli'):
    original_file = df.to_csv(index=False)
    st.download_button(label="Download CSV Asli", data=original_file, file_name="all_data.csv", mime="text/csv")
