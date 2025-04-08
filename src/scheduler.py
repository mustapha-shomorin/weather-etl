import schedule
import time
from src.main import main as job
import logging

logger = logging.getLogger(__name__)

def start_scheduler():
    schedule.every().hour.do(job)
    logger.info("🕒 Scheduler started... Press Ctrl+C to stop.\n")

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduler()
