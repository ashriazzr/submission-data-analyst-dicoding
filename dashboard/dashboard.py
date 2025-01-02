import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('https://raw.githubusercontent.com/ashriazzr/submission-data-analyst-dicoding/refs/heads/main/dashboard/all_data.csv')

season_mapping = {
    1: 'Spring 🌸',
    2: 'Summer ☀️',
    3: 'Autumn 🍂',
    4: 'Winter ❄️'
}
df['Season_Name'] = df['Season'].map(season_mapping)

category_filter = st.selectbox("🔍 Pilih Kategori Analisis", ['Pengaruh Cuaca ☀️🌧️', 'Tren Musiman 🍁❄️'])

if category_filter == 'Pengaruh Cuaca ☀️🌧️':
    filtered_data = df[df['Category'] == 'Weather Impact']
elif category_filter == 'Tren Musiman 🍁❄️':
    filtered_data = df[df['Category'] == 'Seasonal Trend']

st.subheader(f"📋 Data {category_filter}")
st.write(filtered_data)

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

st.pyplot(fig)

if category_filter == 'Pengaruh Cuaca ☀️🌧️':
    st.write("""
        🌞 Dari grafik di atas, kita dapat melihat bahwa jumlah penyewaan sepeda lebih tinggi pada cuaca cerah 
        dan menurun saat cuaca berawan atau hujan. Oleh karena itu, cuaca cerah cenderung meningkatkan minat 
        orang untuk menyewa sepeda.
    """)
elif category_filter == 'Tren Musiman 🍁❄️':
    st.write("""
        🍂 Berdasarkan grafik, terlihat bahwa jumlah penyewaan sepeda paling tinggi pada musim panas ☀️ dan musim gugur 🍁, 
        sementara musim dingin ❄️ memiliki jumlah penyewaan terendah. Hal ini menunjukkan bahwa faktor musim 
        sangat mempengaruhi kebiasaan penyewaan sepeda.
    """)
