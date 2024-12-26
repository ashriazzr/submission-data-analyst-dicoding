import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit layout and title
st.set_page_config(page_title="Air Pollution Analysis", layout="wide")
st.title("Air Pollution Analysis")

# File Upload
st.sidebar.header("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

# Function to determine season based on month
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

# Display instructions if no file is uploaded
if uploaded_file is None:
    st.write("Please upload a CSV file in the sidebar to begin.")
else:
    # Load the uploaded file into a dataframe
    combined_df = pd.read_csv(uploaded_file)
    
    # Data Cleaning and Processing
    st.header("Data Overview")
    st.write("**Initial Dataset**")
    st.write(combined_df.head())
    
    # Handle missing data
    st.write("**Null Value Counts**")
    st.write(combined_df.isnull().sum())
    combined_df_cleaned = combined_df.dropna().copy()

    # Add datetime column
    combined_df_cleaned['datetime'] = pd.to_datetime(combined_df_cleaned[['year', 'month', 'day', 'hour']])
    combined_df_cleaned['Season'] = combined_df_cleaned['datetime'].dt.month.apply(get_season)
    
    # Drop unnecessary columns
    combined_df_cleaned = combined_df_cleaned.drop(columns=['year', 'month', 'day', 'hour', 'No'])

    st.write("**Cleaned Dataset**")
    st.write(combined_df_cleaned.head())
    
    # EDA Section
    st.header("Exploratory Data Analysis")
    
    # Boxplot of PM2.5 by Location
    st.subheader("PM2.5 Distribution by Location")
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Location', y='PM2.5', data=combined_df_cleaned)
    plt.title("PM2.5 Distribution by Location")
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Average PM2.5 by hour
    st.subheader("Average PM2.5 by Hour of the Day")
    hourly_pm25 = combined_df_cleaned.groupby(combined_df_cleaned['datetime'].dt.hour)['PM2.5'].mean()
    fig, ax = plt.subplots(figsize=(12, 6))
    hourly_pm25.plot(kind='bar', ax=ax)
    ax.set_title("Average PM2.5 by Hour")
    ax.set_xlabel("Hour")
    ax.set_ylabel("PM2.5")
    st.pyplot(fig)

    # PM2.5 by Season
    st.subheader("Average PM2.5 by Season")
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Season', y='PM2.5', data=combined_df_cleaned, ci=None)
    plt.title("Average PM2.5 by Season")
    st.pyplot(plt)

    # Correlation Heatmap
    st.subheader("Correlation Heatmap")
    numeric_df = combined_df_cleaned.select_dtypes(include=["float64", "int64"])
    plt.figure(figsize=(10, 8))
    sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Correlation Heatmap")
    st.pyplot(plt)

    # Summary Insights
    st.header("Insights")
    st.markdown("""
    - Certain locations have higher PM2.5 levels than others.
    - PM2.5 levels are generally higher during specific hours of the day (e.g., nighttime).
    - PM2.5 tends to increase during winter.
    - Factors such as temperature, dew point, and rainfall have significant correlations with PM2.5 levels.
    """)
