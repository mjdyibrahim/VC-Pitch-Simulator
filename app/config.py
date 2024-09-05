import os
from dotenv import load_dotenv

load_dotenv()


IBM_API_KEY = os.getenv("IBM_API_KEY")
IBM_CLOUD_URL = os.getenv("IBM_CLOUD_URL")
IBM_PROJECT_ID = os.getenv("IBM_PROJECT_ID")
IBM_SPACE_ID = os.getenv("IBM_SPACE_ID")
