import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Membaca dataset
@st.cache
def load_data():
    return pd.read_csv('../data/PRSA_Data_20130301-20170228.csv')

df = load_data()

# Preprocessing data
df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
df = df.drop(columns=['year', 'month', 'day', 'hour', 'No'])

# Judul Dashboard
st.title("Dashboard Analisis Data Kualitas Udara")

# Visualisasi 1: Pola PM2.5 berdasarkan waktu
st.subheader("Pola PM2.5 Berdasarkan Waktu")
pm25_by_time = df.set_index('datetime')['PM2.5'].resample('M').mean()

fig, ax = plt.subplots(figsize=(10, 6))
pm25_by_time.plot(ax=ax)
ax.set_title("Rata-rata PM2.5 Berdasarkan Bulan")
ax.set_xlabel("Bulan")
ax.set_ylabel("PM2.5")
st.pyplot(fig)

# Visualisasi 2: Korelasi antar variabel
st.subheader("Korelasi Antar Variabel")
correlation = df.corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
st.pyplot(fig)

# Filter interaktif
st.sidebar.header("Filter")
selected_month = st.sidebar.slider("Pilih Bulan (1-12)", 1, 12, 6)
filtered_data = df[df['datetime'].dt.month == selected_month]

st.subheader(f"Data untuk Bulan {selected_month}")
st.write(filtered_data)
