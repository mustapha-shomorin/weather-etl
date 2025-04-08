from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
CITIES = os.getenv("CITIES").split(",")  # Now returns a list
