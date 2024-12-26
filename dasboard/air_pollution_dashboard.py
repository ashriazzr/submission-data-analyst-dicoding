import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import streamlit as st
from google.colab import drive

# Set up Streamlit and Seaborn styling
sns.set(style="whitegrid")
st.set_option('deprecation.showPyplotGlobalUse', False)

# Mount Google Drive for accessing dataset (specific to Google Colab)
drive.mount('/content/drive')

# Data Wrangling - Gathering Data
folder_path = 'https://github.com/ashriazzr/submission-data-analyst-dicoding/tree/main/data'
file_list = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

dataframes = []
for file in file_list:
    df = pd.read_csv(os.path.join(folder_path, file))
    df['Location'] = file.split('_')[2]  # Add Location column based on the file name
    dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)

# Data cleaning: Drop rows with missing values
combined_df_cleaned = combined_df.dropna().copy()

# Convert time-related columns to datetime
datetime_cols = ['year', 'month', 'day', 'hour']
combined_df_cleaned['datetime'] = pd.to_datetime(
    combined_df_cleaned[['year', 'month', 'day', 'hour']].astype(str).agg('-'.join, axis=1)
)

# Sidebar for date selection
min_date = combined_df_cleaned["datetime"].min()
max_date = combined_df_cleaned["datetime"].max()



# Filter data based on the selected date range
main_df = combined_df_cleaned[(combined_df_cleaned["datetime"] >= pd.to_datetime(start_date)) &
                              (combined_df_cleaned["datetime"] <= pd.to_datetime(end_date))]

# Streamlit Dashboard Setup
st.title("Air Pollution Data Analysis")

# Business Questions
st.subheader("Business Questions")
st.write("1. How does the PM2.5 pollution level change across seasons or times of the day?")
st.write("2. Which factors are most strongly correlated with the PM2.5 levels?")

# Analyzing PM2.5 pollution level over time
st.subheader("PM2.5 Pollution Over Time")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=main_df, x="datetime", y="PM2.5", marker="o", linewidth=2, color="#FF7043")
plt.title("PM2.5 Pollution Over Time")
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

# Correlation between factors and PM2.5
st.subheader("Correlation with PM2.5 Levels")
correlation_df = main_df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']]
corr_matrix = correlation_df.corr()

fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=1, ax=ax)
plt.title("Correlation Matrix of Factors with PM2.5")
st.pyplot(fig)

# Average PM2.5 levels by Location
st.subheader("Average PM2.5 by Location")
avg_pm25_by_location = main_df.groupby('Location')['PM2.5'].mean().reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x="Location", y="PM2.5", data=avg_pm25_by_location, palette="viridis")
plt.title("Average PM2.5 Levels by Location")
ax.tick_params(axis='x', rotation=45, labelsize=12)
ax.tick_params(axis='y', labelsize=12)
st.pyplot(fig)

# Pollution by Hour of the Day
st.subheader("PM2.5 Pollution by Hour of the Day")
hourly_pm25 = main_df.groupby('hour')['PM2.5'].mean().reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=hourly_pm25, x='hour', y='PM2.5', marker="o", linewidth=2, color="#66BB6A")
plt.title("PM2.5 Levels by Hour of the Day")
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

# Display additional insights
st.caption('Copyright (C) ASHRI AULIA AZZAHRA 2024')

