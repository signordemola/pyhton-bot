import logging
from bot.app import create_bot

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    """Main application entry point"""
    logger = logging.getLogger(__name__)

    try:
        bot_app = create_bot()
        logger.info("Starting bot...")
        bot_app.run_polling()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise


if __name__ == "__main__":
    main()