import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Production AI Agent API"
    DB_URI: str = os.getenv("DB_URI", "postgresql://postgres:postgres@localhost:5432/ai_agent_db")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

settings = Settings()