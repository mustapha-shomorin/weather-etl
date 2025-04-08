
from config.settings import API_KEY, CITIES
from etl import get_weather, transform_weather_data, save_to_db
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    all_data = []
    for city in CITIES:
        try:
            logger.info(f"Fetching weather for {city}...")
            data = get_weather(city, API_KEY)
            if data.get("cod") == 200:
                record = transform_weather_data([data])
                all_data.append(record[0])
            else:
                logger.warning(f"Failed to fetch data for {city}: {data.get('message')}")
        except Exception as e:
            logger.error(f"Exception occurred for {city}: {e}")

    if not all_data:
        logger.warning("⚠️ No data collected.")
        return

    df = pd.DataFrame(all_data)

    try:
        df.to_csv("weather_data.csv", index=False)
        logger.info("✅ Data saved to weather_data.csv")
    except Exception as e:
        logger.error(f"Failed to save CSV: {e}")

    try:
        save_to_db(df)
    except Exception as e:
        logger.error(f"Failed to save to DB: {e}")

if __name__ == "__main__":
    main()

