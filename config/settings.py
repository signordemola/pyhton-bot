import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    ADMIN_IDS = [int(x) for x in os.getenv('ADMIN_USER_IDS', '').split(',') if x.strip()]
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot.db')

    @classmethod
    def validate(cls):
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required")


Config.validate()
settings = Config()