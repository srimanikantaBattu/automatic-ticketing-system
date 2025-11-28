import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Smart Ticketing Automation Platform"
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "smart_ticketing_db")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    
settings = Settings()
