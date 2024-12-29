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

# Fitur untuk filter data berdasarkan nilai dalam kolom tertentu
column_to_filter = st.selectbox("Pilih kolom untuk filter:", df.columns)

if column_to_filter:
    # Menampilkan nilai unik dalam kolom yang dipilih
    unique_values = df[column_to_filter].unique()
    value_to_filter = st.selectbox(f"Pilih nilai untuk filter di kolom {column_to_filter}:", unique_values)

    # Filter data berdasarkan pilihan pengguna
    filtered_df = df[df[column_to_filter] == value_to_filter]
    st.subheader(f"Data yang Terfilter berdasarkan {column_to_filter} = {value_to_filter}")
    st.write(filtered_df)

# Statistik deskriptif
st.subheader("Statistik Deskriptif Data Numerik")
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
if len(numeric_columns) > 0:
    st.write(df[numeric_columns].describe())
else:
    st.write("Tidak ada kolom numerik untuk statistik deskriptif.")

# Visualisasi Data yang Lebih Baik
st.subheader("Visualisasi Data")
# Memilih kolom untuk visualisasi
chart_column = st.selectbox("Pilih kolom untuk visualisasi:", df.columns)

if chart_column:
    # Plot data dengan gaya seaborn
    fig, ax = plt.subplots(figsize=(10, 6))  # Menambah ukuran gambar untuk kenyamanan
    if df[chart_column].dtype in ['int64', 'float64']:  # Numeric columns
        sns.histplot(df[chart_column].dropna(), bins=20, kde=True, color='skyblue', edgecolor='black', ax=ax)
        ax.set_title(f"Distribusi {chart_column}", fontsize=16)
        ax.set_xlabel(chart_column, fontsize=14)
        ax.set_ylabel('Frekuensi', fontsize=14)
    else:  # Categorical columns
        value_counts = df[chart_column].value_counts()
        sns.barplot(x=value_counts.index, y=value_counts.values, palette='Blues_d', ax=ax)
        ax.set_title(f"Distribusi {chart_column}", fontsize=16)
        ax.set_xlabel(chart_column, fontsize=14)
        ax.set_ylabel('Jumlah', fontsize=14)
    
    st.pyplot(fig)

# Menjawab Pertanyaan 1: Apakah Cuaca (Weather, Temperature, Humidity) Memengaruhi Jumlah Penyewaan Sepeda?
st.subheader("Pengaruh Cuaca terhadap Penyewaan Sepeda")

# Plot scatter untuk melihat hubungan antara suhu, kelembapan dan jumlah penyewaan sepeda
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x=df['temperature'], y=df['count'], hue=df['weather'], palette='coolwarm', ax=ax)
ax.set_title("Hubungan antara Suhu dan Jumlah Penyewaan Sepeda berdasarkan Cuaca", fontsize=16)
ax.set_xlabel('Suhu (°C)', fontsize=14)
ax.set_ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
st.pyplot(fig)

# Jika ada data kelembapan, kita juga bisa menambahkannya
if 'humidity' in df.columns:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x=df['humidity'], y=df['count'], hue=df['weather'], palette='coolwarm', ax=ax)
    ax.set_title("Hubungan antara Kelembapan dan Jumlah Penyewaan Sepeda berdasarkan Cuaca", fontsize=16)
    ax.set_xlabel('Kelembapan (%)', fontsize=14)
    ax.set_ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
    st.pyplot(fig)

# Menjawab Pertanyaan 2: Bagaimana Tren Penyewaan Sepeda Berdasarkan Musim?
st.subheader("Tren Penyewaan Sepeda Berdasarkan Musim")

# Misalkan kolom 'season' ada dalam dataset, kita buat boxplot berdasarkan musim
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x=df['season'], y=df['count'], palette='Set2', ax=ax)
ax.set_title("Tren Penyewaan Sepeda Berdasarkan Musim", fontsize=16)
ax.set_xlabel('Musim', fontsize=14)
ax.set_ylabel('Jumlah Penyewaan Sepeda', fontsize=14)
st.pyplot(fig)

# Fitur rentang tanggal (jika ada kolom bertipe datetime)
if 'date' in df.columns or 'tanggal' in df.columns:  # Asumsi ada kolom bertipe tanggal
    df['tanggal'] = pd.to_datetime(df['tanggal'], errors='coerce')
    start_date, end_date = st.date_input("Pilih rentang tanggal", 
                                        [df['tanggal'].min(), df['tanggal'].max()])
    filtered_df_by_date = df[(df['tanggal'] >= pd.to_datetime(start_date)) & 
                             (df['tanggal'] <= pd.to_datetime(end_date))]
    st.write(filtered_df_by_date)

# Tabel Pivot
st.subheader("Tabel Pivot")
# Pilih dua kolom untuk pivot
pivot_columns = df.select_dtypes(include=['object', 'category']).columns
pivot_index = st.selectbox("Pilih kolom untuk baris pivot:", pivot_columns)
pivot_columns_2 = st.selectbox("Pilih kolom untuk kolom pivot:", pivot_columns)

if pivot_index and pivot_columns_2:
    pivot_df = df.pivot_table(index=pivot_index, columns=pivot_columns_2, aggfunc='count', fill_value=0)
    st.write(pivot_df)

# Menyediakan tombol untuk mendownload data yang terfilter
if st.button('Download Data yang Terfilter'):
    filtered_file = filtered_df.to_csv(index=False)
    st.download_button(label="Download CSV", data=filtered_file, file_name="filtered_data.csv", mime="text/csv")

# Menyediakan tombol untuk mendownload data asli
if st.button('Download Data Asli'):
    original_file = df.to_csv(index=False)
    st.download_button(label="Download CSV Asli", data=original_file, file_name="all_data.csv", mime="text/csv")
