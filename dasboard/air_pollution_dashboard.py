import streamlit as st
import pandas as pd
import os

# Path ke data
DATA_PATH = "./main_data.csv"

# Cek apakah file ada
if os.path.exists(DATA_PATH):
    # Baca file CSV
    try:
        data = pd.read_csv(DATA_PATH)
        st.success("Data berhasil di-load!")
        st.write(data.head())  # Tampilkan beberapa baris data
    except Exception as e:
        st.error(f"Error saat membaca data: {e}")
else:
    st.error(f"File {DATA_PATH} tidak ditemukan. Pastikan file ada di folder yang benar.")
