import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_MODE = os.getenv("DATABASE_MODE", "json")
DATABASE_URL = os.getenv("DATABASE_URL")