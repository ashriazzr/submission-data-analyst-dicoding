import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('all_data.csv')

st.title("Analisis Penyewaan Sepeda Berdasarkan Cuaca dan Musim")
st.write("""
    Aplikasi ini menunjukkan bagaimana cuaca dan musim memengaruhi jumlah penyewaan sepeda. 
    Gunakan filter untuk memilih kategori yang ingin dianalisis.
""")

category_filter = st.selectbox("Pilih Kategori Analisis", ['Weather Impact', 'Seasonal Trend'])

filtered_data = df[df['Category'] == category_filter]

st.subheader(f"Data {category_filter}")
st.write(filtered_data)

st.subheader(f"Visualisasi {category_filter}")

fig, ax = plt.subplots(figsize=(10, 6))

if category_filter == 'Weather Impact':
    sns.barplot(x='Weather_Situation', y='Average_Rentals', data=filtered_data, ax=ax)
    ax.set_title("Pengaruh Cuaca Terhadap Penyewaan Sepeda")
    ax.set_xlabel("Situasi Cuaca")
    ax.set_ylabel("Rata-Rata Penyewaan")
    ax.set_xticklabels(['Cerah', 'Berawan', 'Hujan'])
    
elif category_filter == 'Seasonal Trend':
    sns.barplot(x='Season', y='Average_Rentals', data=filtered_data, ax=ax)
    ax.set_title("Tren Penyewaan Sepeda Berdasarkan Musim")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-Rata Penyewaan")
    ax.set_xticklabels(['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'])

st.pyplot(fig)

if category_filter == 'Weather Impact':
    st.write("""
        Dari grafik di atas, kita dapat melihat bahwa jumlah penyewaan sepeda lebih tinggi pada cuaca cerah 
        (situasi cuaca 1) dan menurun saat cuaca berawan (situasi cuaca 2) atau hujan (situasi cuaca 3).
    """)
elif category_filter == 'Seasonal Trend':
    st.write("""
        Berdasarkan grafik, terlihat bahwa jumlah penyewaan sepeda paling tinggi pada musim panas (season 2) 
        dan musim gugur (season 3), sementara musim dingin (season 4) memiliki jumlah penyewaan terendah.
    """)
