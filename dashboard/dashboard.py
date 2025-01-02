import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Membaca data dari CSV
df = pd.read_csv('https://raw.githubusercontent.com/ashriazzr/submission-data-analyst-dicoding/refs/heads/main/dashboard/all_data.csv')

# Mengganti nilai numerik di kolom Season dengan nama musim
season_mapping = {
    1: 'Spring 🌸',
    2: 'Summer ☀️',
    3: 'Autumn 🍂',
    4: 'Winter ❄️'
}
df['Season_Name'] = df['Season'].map(season_mapping)

# Menampilkan struktur data setelah perubahan
st.write("Data yang telah dimodifikasi:")
st.write(df[['Weather_Situation', 'Average_Rentals', 'Category', 'Season_Name']].head())

# Filter kategori yang dipilih
category_filter = st.selectbox("🔍 Pilih Kategori Analisis", ['Pengaruh Cuaca ☀️🌧️', 'Tren Musiman 🍁❄️'])

# Menyaring data berdasarkan kategori yang dipilih
if category_filter == 'Pengaruh Cuaca ☀️🌧️':
    filtered_data = df[df['Category'] == 'Weather Impact']
elif category_filter == 'Tren Musiman 🍁❄️':
    filtered_data = df[df['Category'] == 'Seasonal Trend']

# Menampilkan data yang difilter
st.subheader(f"📋 Data {category_filter}")
st.write(filtered_data)

# Visualisasi berdasarkan kategori yang dipilih
fig, ax = plt.subplots(figsize=(10, 6))

if category_filter == 'Pengaruh Cuaca ☀️🌧️':
    sns.barplot(x='Weather_Situation', y='Average_Rentals', data=filtered_data, ax=ax, palette="coolwarm")
    ax.set_title("💨 Pengaruh Cuaca Terhadap Penyewaan Sepeda", fontsize=16)
    ax.set_xlabel("Situasi Cuaca 🌤️", fontsize=14)
    ax.set_ylabel("Rata-Rata Penyewaan 🚲", fontsize=14)
    ax.set_xticklabels(['Cerah ☀️', 'Berawan 🌥️', 'Hujan 🌧️'], fontsize=12)
    
elif category_filter == 'Tren Musiman 🍁❄️':
    sns.barplot(x='Season_Name', y='Average_Rentals', data=filtered_data, ax=ax, palette="Set2")
    ax.set_title("🌳 Tren Penyewaan Sepeda Berdasarkan Musim", fontsize=16)
    ax.set_xlabel("Musim 🌸", fontsize=14)
    ax.set_ylabel("Rata-Rata Penyewaan 🚲", fontsize=14)
    ax.set_xticklabels(['Spring 🌸', 'Summer ☀️', 'Autumn 🍂', 'Winter ❄️'], fontsize=12)

# Menampilkan grafik
st.pyplot(fig)
