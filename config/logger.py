import logging
from pathlib import Path

# Ensure logs directory exists
Path("logs").mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    filename='logs/etl.log',
    level=logging.INFO,
    format='%(asctime)s — %(levelname)s — %(name)s — %(message)s',
    filemode='a'
)

logger = logging.getLogger('weather_etl')
