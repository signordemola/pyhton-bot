import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot.db')

    admin_ids_str = os.getenv('ADMIN_USER_IDS', '')
    if admin_ids_str.strip():
        ADMIN_IDS = [int(x.strip()) for x in admin_ids_str.split(',') if x.strip()]
    else:
        ADMIN_IDS = []

    @classmethod
    def validate(cls):
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required")


Config.validate()
settings = Config()