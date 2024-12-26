import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="Dashboard Udara", layout="wide")

# Title and description
st.title("Dashboard Analisis Data Udara")
st.write("Analisis data kualitas udara dengan visualisasi interaktif.")

# Upload data
uploaded_file = st.file_uploader("Unggah file dataset (CSV):", type=["csv"])
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("### Dataframe")
    st.dataframe(data)

    # Sidebar options
    st.sidebar.header("Pengaturan Visualisasi")
    selected_columns = st.sidebar.multiselect("Pilih kolom untuk korelasi:", data.columns)

    if selected_columns:
        # Correlation heatmap
        st.write("### Heatmap Korelasi")
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(data[selected_columns].corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        st.pyplot(fig)

    # Histogram
    st.write("### Histogram")
    selected_column = st.sidebar.selectbox("Pilih kolom untuk histogram:", data.columns)
    bins = st.sidebar.slider("Jumlah bins:", min_value=5, max_value=50, value=20)
    fig, ax = plt.subplots()
    data[selected_column].hist(bins=bins, ax=ax)
    st.pyplot(fig)

    # Scatter plot
    st.write("### Scatter Plot")
    x_axis = st.sidebar.selectbox("Pilih sumbu X:", data.columns)
    y_axis = st.sidebar.selectbox("Pilih sumbu Y:", data.columns)
    fig, ax = plt.subplots()
    ax.scatter(data[x_axis], data[y_axis])
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    st.pyplot(fig)

else:
    st.write("Unggah file CSV untuk memulai.")

# Footer
st.markdown("---")
st.markdown("Dibuat dengan ❤️ oleh [Nama Anda]")
