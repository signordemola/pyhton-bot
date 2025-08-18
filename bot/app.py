import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config.settings import settings
from bot.handlers.commands import start, help_command
from bot.handlers.callbacks import handle_menu

logger = logging.getLogger(__name__)

def create_bot() -> Application:
    """Create and configure the bot application"""
    app = Application.builder().token(settings.BOT_TOKEN).build()

    # All handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))
    

    logger.info("Bot application configured successfully")
    return app