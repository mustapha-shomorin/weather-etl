
import requests
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from pathlib import Path
import logging
from config.logger import logger


logger = logging.getLogger(__name__)

def get_weather(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

def transform_weather_data(data_list):
    records = []
    category_map = {
        "Clear": "Dry", "Clouds": "Overcast", "Rain": "Wet",
        "Drizzle": "Wet", "Thunderstorm": "Storm", "Snow": "Cold",
        "Mist": "Humid", "Haze": "Humid", "Fog": "Humid",
        "Dust": "Dry", "Sand": "Dry", "Ash": "Hazard",
        "Squall": "Windy", "Tornado": "Extreme"
    }

    for data in data_list:
        utc_dt = datetime.utcfromtimestamp(data['dt'])
        timezone_offset = data.get('timezone', 0)
        local_dt = utc_dt + timedelta(seconds=timezone_offset)
        sunrise = datetime.utcfromtimestamp(data['sys']['sunrise']) + timedelta(seconds=timezone_offset)
        sunset = datetime.utcfromtimestamp(data['sys']['sunset']) + timedelta(seconds=timezone_offset)
        is_day = sunrise <= local_dt <= sunset
        weather_main = data['weather'][0]['main']
        weather_category = category_map.get(weather_main, "Other")

        records.append({
            "city": data['name'],
            "country": data['sys']['country'],
            "local_time": local_dt.strftime('%Y-%m-%d %H:%M:%S'),
            "is_daytime": is_day,
            "weather_main": weather_main,
            "weather_category": weather_category,
            "temp": data['main']['temp'],
            "humidity": data['main']['humidity'],
            "wind_speed": data['wind']['speed'],
            "pressure": data['main']['pressure'],
            "data_collected_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        })

    return records

def save_to_db(df: pd.DataFrame, db_path='data/weather_data.db', table_name='weather'):
    Path("data").mkdir(exist_ok=True)
    engine = create_engine(f'sqlite:///{db_path}')
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
    logger.info(f"✅ Data saved to {db_path} in table '{table_name}'")
