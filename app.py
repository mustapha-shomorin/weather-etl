import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime

sns.set(style="whitegrid")

@st.cache_data
def load_data():
    conn = sqlite3.connect("data/weather_data.db")
    df = pd.read_sql_query("SELECT * FROM weather", conn)
    conn.close()
    
    # Convert time columns
    df['local_time'] = pd.to_datetime(df['local_time'])
    df['is_daytime'] = df['is_daytime'].astype(bool)
    return df

df = load_data()

st.sidebar.title("🔍 Filters")

# City filter
cities = st.sidebar.multiselect("Select City", options=df['city'].unique(), default=df['city'].unique())

# Date range filter
min_date = df['local_time'].min().date()
max_date = df['local_time'].max().date()
start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date])

# Apply filters
filtered_df = df[
    (df['city'].isin(cities)) & 
    (df['local_time'].dt.date >= start_date) &
    (df['local_time'].dt.date <= end_date)
]

st.title("⛅ Real-Time Weather Dashboard")
st.markdown("An interactive dashboard for weather ETL data with city & date filters.")

st.subheader("🌡️ Temperature Trend")
fig1, ax1 = plt.subplots(figsize=(12, 5))
sns.lineplot(data=filtered_df, x='local_time', y='temp', hue='city', marker='o', ax=ax1)
ax1.set_xlabel("Time")
ax1.set_ylabel("Temperature (°C)")
plt.xticks(rotation=45)
st.pyplot(fig1)

st.subheader("💧 Humidity by City")
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.boxplot(data=filtered_df, x='city', y='humidity', palette='coolwarm', ax=ax2)
st.pyplot(fig2)

st.subheader("🌦️ Weather Category Counts")
fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.countplot(data=filtered_df, x='weather_category', hue='city', palette='Set2', ax=ax3)
plt.xticks(rotation=45)
st.pyplot(fig3)

st.subheader("☀️🌙 Daytime vs Nighttime")
fig4, ax4 = plt.subplots(figsize=(8, 5))
sns.countplot(data=filtered_df, x='is_daytime', hue='city', palette='viridis', ax=ax4)
ax4.set_xticklabels(['Night', 'Day'])
st.pyplot(fig4)
