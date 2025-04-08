import pandas as pd
from sqlalchemy import create_engine
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

def weather_category_counts(df):
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='weather_category', hue='city', palette='Set2')

    plt.title("🌦️ Weather Category Counts by City", fontsize=16)
    plt.xlabel("Weather Category")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("visuals/weather_category_counts.png")
    plt.show()

def day_night_observations(df):
    plt.figure(figsize=(8, 6))
    sns.countplot(data=df, x='is_daytime', hue='city', palette='viridis')

    plt.title("☀️🌙 Daytime vs Nighttime Observations", fontsize=16)
    plt.xlabel("Is Daytime?")
    plt.ylabel("Count")
    plt.xticks([0, 1], ['Night', 'Day'])  # Convert boolean to readable labels
    plt.tight_layout()
    plt.savefig("visuals/day_night_observations.png")
    plt.show()

def temp_trend_by_city(df):
    # Suppress all warnings
    warnings.filterwarnings("ignore")

    # Set plot style
    sns.set(style="whitegrid")

    # Plot temperature trends
    plt.figure(figsize=(14, 6))
    sns.lineplot(data=df, x='local_time', y='temp', hue='city', marker='o')

    plt.title("🌡️ Temperature Trend Over Time by City", fontsize=16)
    plt.xlabel("Local Time")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("visuals/temp_trend_by_city.png")
    plt.show()

def avg_humidity_by_city(df):
    plt.figure(figsize=(10, 5))
    avg_humidity = df.groupby("city")["humidity"].mean().sort_values()
    sns.barplot(x=avg_humidity.index, y=avg_humidity.values, palette="coolwarm")

    plt.title("💧 Average Humidity by City", fontsize=16)
    plt.ylabel("Average Humidity (%)")
    plt.xlabel("City")
    plt.tight_layout()
    plt.savefig("visuals/avg_humidity_by_city.png")  # Save plot
    plt.show()

def load_sqlite_data(engine = create_engine('sqlite:///data/weather_dataa.db')):
    # Load the data
    df = pd.read_sql("SELECT * FROM weather", con=engine)
    # Convert datetime columns to proper datetime format
    df['local_time'] = pd.to_datetime(df['local_time'])
    df['data_collected_at'] = pd.to_datetime(df['data_collected_at'])

    return df

