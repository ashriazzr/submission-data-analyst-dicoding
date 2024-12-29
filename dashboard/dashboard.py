import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul aplikasi
st.title("Aplikasi Streamlit untuk Mengelola Data CSV")

# URL file CSV di GitHub
url = "https://raw.githubusercontent.com/ashriazzr/submission-data-analyst-dicoding/refs/heads/main/dashboard/all_data.csv"

# Membaca CSV dari URL
df = pd.read_csv(url)

# Menampilkan data
st.subheader("Data yang Diupload")
st.write(df)

# Pertanyaan 1: Apakah cuaca (weather, temperature, humidity) memengaruhi jumlah penyewaan sepeda?

st.subheader("Apakah Cuaca (Weather, Temperature, Humidity) Memengaruhi Jumlah Penyewaan Sepeda?")
# Visualisasi hubungan antara cuaca, suhu, kelembapan dan jumlah penyewaan sepeda
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# 1. Cuaca vs Penyewaan Sepeda
sns.boxplot(data=df, x='weather', y='rentals', ax=axes[0])
axes[0].set_title('Cuaca vs Penyewaan Sepeda')
axes[0].set_xlabel('Cuaca')
axes[0].set_ylabel('Jumlah Penyewaan Sepeda')

# 2. Suhu vs Penyewaan Sepeda
sns.scatterplot(data=df, x='temperature', y='rentals', ax=axes[1], color='orange')
axes[1].set_title('Suhu vs Penyewaan Sepeda')
axes[1].set_xlabel('Suhu (°C)')
axes[1].set_ylabel('Jumlah Penyewaan Sepeda')

# 3. Kelembapan vs Penyewaan Sepeda
sns.scatterplot(data=df, x='humidity', y='rentals', ax=axes[2], color='green')
axes[2].set_title('Kelembapan vs Penyewaan Sepeda')
axes[2].set_xlabel('Kelembapan (%)')
axes[2].set_ylabel('Jumlah Penyewaan Sepeda')

st.pyplot(fig)

# Pertanyaan 2: Bagaimana tren penyewaan sepeda berdasarkan musim (season)?

st.subheader("Tren Penyewaan Sepeda Berdasarkan Musim (Season)")
# Visualisasi tren penyewaan sepeda berdasarkan musim
fig2, ax2 = plt.subplots(figsize=(10, 6))

sns.boxplot(data=df, x='season', y='rentals', ax=ax2, palette='coolwarm')
ax2.set_title('Tren Penyewaan Sepeda Berdasarkan Musim')
ax2.set_xlabel('Musim')
ax2.set_ylabel('Jumlah Penyewaan Sepeda')

st.pyplot(fig2)

# Menyediakan tombol untuk mendownload data yang terfilter
if st.button('Download Data yang Terfilter'):
    filtered_file = df.to_csv(index=False)
    st.download_button(label="Download CSV", data=filtered_file, file_name="filtered_data.csv", mime="text/csv")

# Menyediakan tombol untuk mendownload data asli
if st.button('Download Data Asli'):
    original_file = df.to_csv(index=False)
    st.download_button(label="Download CSV Asli", data=original_file, file_name="all_data.csv", mime="text/csv")
