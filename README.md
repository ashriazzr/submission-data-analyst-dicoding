# Bike Sharing Dataset Analysis with Python - Dicoding

Bike Sharing Dataset Dashboard

[Bike Sharing Dataset Dashboard Streamlit App](https://submission-data-analyst-dicoding-24.streamlit.app/)

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Data Sources](#data-sources)

## Overview

Proyek ini melibatkan analisis dan visualisasi Dataset Bike Sharing, dengan mencakup teknik-teknik untuk pengolahan data, analisis data eksploratif (EDA), dan pengembangan dasbor interaktif menggunakan Streamlit untuk mempermudah eksplorasi data. Tujuan proyek ini adalah untuk mendapatkan wawasan dari data Bike Sharing melalui analisis yang komprehensif.

## Project Structure

- `dashboard/`: This directory contains dashboard.py which is used to create dashboards of data analysis results.
- `data/`: Directory containing the raw CSV data files.
- `notebook.ipynb`: This file is used to perform data analysis.
- `README.md`: This documentation file.


```plaintext
submission-data-analyst-dicoding/
├───dashboard/
│   ├───all_data.csv         
│   └───dashboard.py        
├───data/
│   ├───day.csv              
│   └───hour.csv             
├───notebook.ipynb           
├───README.md                
├───requirements.txt         
└───url.txt                  

```
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

2. **Exploratory Data Analysis (EDA)**: Explore and analyze the data using the provided Python scripts. EDA insights can guide your understanding of Bike Sharing Dataset patterns.

3. **Visualization**: Run the Streamlit dashboard for interactive data exploration:

```
cd submission-data-analyst-dicoding/dashboard
streamlit run dashboard.py
```

Access the dashboard in your web browser at `http://localhost:8501`.

## Data Sources

The project uses Bike Sharing Dataset from [Belajar Analisis Data dengan Python's Final Project](https://drive.google.com/file/d/1RaBmV6Q6FYWU4HWZs80Suqd7KQC34diQ/view) offered by [Dicoding](https://www.dicoding.com/).

© Ashri Aulia Azzahra 2024. All rights reserved.
