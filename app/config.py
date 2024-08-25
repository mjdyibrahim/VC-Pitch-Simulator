import os
from dotenv import load_dotenv

load_dotenv()


IBM_API_KEY = os.getenv("IBM_API_KEY")
IBM_CLOUD_URL = os.getenv("IBM_CLOUD_URL")
PROJECT_ID = os.getenv("PROJECT_ID")
