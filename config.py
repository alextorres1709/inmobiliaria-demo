import os
from dotenv import load_dotenv

load_dotenv()

_default_db = "sqlite:///demo_inmobiliaria.db"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "demo-secret-key-2024")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", _default_db)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {}
    SEND_FILE_MAX_AGE_DEFAULT = 3600
    ADMIN_EMAIL = "demo@asentis.es"
    ADMIN_PASSWORD = "demo123"
    API_KEY = "immo-demo-api-key"
    OPENAI_API_KEY = ""
    TELEGRAM_BOT_TOKEN = ""
