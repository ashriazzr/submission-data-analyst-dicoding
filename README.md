# E-Commerce Public Data Analysis with Python - Dicoding

![E-Commerce Data Dashboard](dashboard.gif)

[E-Commerce Data Dashboard Streamlit App](https://submission-data-analyst-dicoding.streamlit.app/)

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Data Sources](#data-sources)

## Overview

This project focuses on data analysis and visualization centered around air quality public data. It includes code for data preprocessing, exploratory data analysis (EDA), and a Streamlit dashboard for interactive exploration of air quality metrics. The goal of this project is to analyze data from public air quality datasets to gain insights into environmental conditions and pollution levels.

## Project Structure

- `dashboard/`: This directory contains dashboard.py which is used to create dashboards of data analysis results.
- `data/`: Directory containing the raw CSV data files.
- `notebook.ipynb`: This file is used to perform data analysis.
- `notebook_EN.ipynb`: notebook.ipynb in English.
- `README.md`: This documentation file.

## Installation

1. Clone this repository to your local machine:

```
git clone https://github.com/ashriazzr/submission-data-analyst-dicoding.git
```

2. Go to the project directory

```
cd data-analyst-dicoding
```

3. Install the required Python packages by running:

```
pip install -r requirements.txt
```

## Usage

1. **Data Wrangling**: Data wrangling scripts are available in the `notebook.ipynb` file to prepare and clean the data.

2. **Exploratory Data Analysis (EDA)**: Explore and analyze the data using the provided Python scripts. EDA insights can guide your understanding of e-commerce public data patterns.

3. **Visualization**: Run the Streamlit dashboard for interactive data exploration:

```
cd data-analyst-dicoding/dashboard
streamlit run air-pollution-dashboard.py
```

Access the dashboard in your web browser at `http://localhost:8501`.

## Data Sources

The project uses E-Commerce Public Dataset from [Belajar Analisis Data dengan Python's Final Project](https://drive.google.com/file/d/1RhU3gJlkteaAQfyn9XOVAz7a5o1-etgr/view) offered by [Dicoding](https://www.dicoding.com/).
