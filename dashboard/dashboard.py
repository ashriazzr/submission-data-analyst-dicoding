import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data
def load_data(url):
    """
    Memuat data dari URL dan menggunakan cache untuk optimisasi performa.
    """
    try:
        data = pd.read_csv(url)
        return data
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

# Memuat dataset
main_data = load_data('https://raw.githubusercontent.com/ashriazzr/submission-data-analyst-dicoding/refs/heads/main/dashboard/all_data.csv')

# Cek apakah data berhasil dimuat
if main_data.empty:
    st.error("Dataset is empty. Please check the URL or data source.")
else:
    st.success("Data loaded successfully!")

# Pertanyaan 1: Apakah Cuaca (Weather, Temperature, Humidity) Memengaruhi Jumlah Penyewaan Sepeda?
st.title("✨ Bike Sharing Dashboard")

# Memisahkan data untuk analisis cuaca
st.header("🌞 Impact of Weather on Bike Rentals")

# Memeriksa kolom yang ada dalam dataset
st.write(main_data.columns)

# Scatter plot untuk Temperature vs Rentals, pastikan 'weather' ada
if 'weather' in main_data.columns:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=main_data, x='temp', y='cnt', hue='weather', palette='coolwarm', ax=ax)
    ax.set_title("Temperature vs Bike Rentals by Weather", fontsize=14)
    ax.set_xlabel("Temperature (Normalized)", fontsize=12)
    ax.set_ylabel("Number of Bike Rentals", fontsize=12)
    st.pyplot(fig)
else:
    st.warning("The 'weather' column is missing or invalid. Please check your data.")


# Scatter plot untuk Humidity vs Rentals
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=main_data, x='hum', y='cnt', hue='weather', palette='coolwarm', ax=ax2)
ax2.set_title("Humidity vs Bike Rentals by Weather", fontsize=14)
ax2.set_xlabel("Humidity (Normalized)", fontsize=12)
ax2.set_ylabel("Number of Bike Rentals", fontsize=12)
st.pyplot(fig2)

# Heatmap untuk pengaruh suhu dan kelembapan terhadap penyewaan
main_data['temp_group'] = pd.cut(main_data['temp'], bins=3, labels=['Low', 'Medium', 'High'])
main_data['hum_group'] = pd.cut(main_data['hum'], bins=3, labels=['Low', 'Medium', 'High'])
avg_rental_by_weather = main_data.groupby(['temp_group', 'hum_group'], observed=True)['cnt'].mean().unstack()

# Heatmap
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.heatmap(avg_rental_by_weather, annot=True, cmap='coolwarm', fmt=".2f", ax=ax3)
ax3.set_title('Average Bike Rentals Based on Temperature and Humidity', fontsize=14)
ax3.set_xlabel('Humidity Group', fontsize=12)
ax3.set_ylabel('Temperature Group', fontsize=12)
st.pyplot(fig3)

# Pertanyaan 2: Tren Penyewaan Sepeda Berdasarkan Musim
st.header("📈 Seasonal Bike Rental Trends")

# Grouping berdasarkan musim dan menghitung rata-rata penyewaan per musim
seasonal_rentals = main_data.groupby('season')['cnt'].mean()

# Line plot tren penyewaan per musim
fig4, ax4 = plt.subplots(figsize=(10, 6))
seasonal_rentals.plot(kind='bar', ax=ax4, color='skyblue', edgecolor='black')
ax4.set_title("Average Bike Rentals by Season", fontsize=14)
ax4.set_xlabel("Season", fontsize=12)
ax4.set_ylabel("Average Bike Rentals", fontsize=12)
st.pyplot(fig4)
