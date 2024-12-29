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

# Memeriksa nama kolom untuk memastikan 'weather' ada
st.write("Kolom yang Tersedia: ", df.columns)

# Periksa apakah 'weather' ada atau menggunakan nama lain, misalnya 'weather_condition'
if 'weather' in df.columns:
    df['weather'] = df['weather'].astype('category')
elif 'weather_condition' in df.columns:
    df['weather_condition'] = df['weather_condition'].astype('category')

# Mengonversi kolom 'rentals' menjadi numerik
df['rentals'] = pd.to_numeric(df['rentals'], errors='coerce')

# Menghapus data yang hilang
df = df.dropna(subset=['weather', 'rentals'])

# Memeriksa nilai unik dalam kolom 'weather' atau 'weather_condition'
st.write(df['weather'].unique() if 'weather' in df.columns else df['weather_condition'].unique())

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

# Menyediakan tombol untuk mendownload data yang terfilter
if st.button('Download Data yang Terfilter'):
    filtered_file = df.to_csv(index=False)
    st.download_button(label="Download CSV", data=filtered_file, file_name="filtered_data.csv", mime="text/csv")

# Menyediakan tombol untuk mendownload data asli
if st.button('Download Data Asli'):
    original_file = df.to_csv(index=False)
    st.download_button(label="Download CSV Asli", data=original_file, file_name="all_data.csv", mime="text/csv")
