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

# Visualisasi Data
st.subheader("Visualisasi Data")
# Memilih kolom untuk visualisasi
chart_column = st.selectbox("Pilih kolom untuk visualisasi:", df.columns)

if chart_column:
    # Plot data
    fig, ax = plt.subplots()
    if df[chart_column].dtype in ['int64', 'float64']:  # Numeric columns
        ax.hist(df[chart_column].dropna(), bins=20, color='skyblue', edgecolor='black')
        ax.set_title(f"Distribusi {chart_column}")
        ax.set_xlabel(chart_column)
        ax.set_ylabel('Frekuensi')
    else:  # Categorical columns
        value_counts = df[chart_column].value_counts()
        ax.bar(value_counts.index, value_counts.values, color='lightcoral')
        ax.set_title(f"Distribusi {chart_column}")
        ax.set_xlabel(chart_column)
        ax.set_ylabel('Jumlah')
    
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


modifikasi ini menjadi visual yang menjawab pertanyaaan in berdasarkan data hasil deploy yang saya punya all_data.csv
Pertanyaan 1 : Apakah cuaca (weather, temperature, humidity) memengaruhi jumlah penyewaan sepeda?
Pertanyaan 2 : Bagaimana tren penyewaan sepeda berdasarkan musim (season)?
