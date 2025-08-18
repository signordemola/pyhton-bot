from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards.menu import main_menu
from config.settings import settings


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        welcome_text = f"""
        🎉 Welcome to Our Bot, {user.first_name}!
        """
        await update.message.reply_text(welcome_text.strip(), reply_markup=main_menu())
    except Exception as e:
        if settings.debug:
            print(f"Error in start: {e}")
        await update.message.reply_text("Something went wrong. Try again later.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        help_text = """
        🤖 Bot Commands:
        
        /start - Start the bot and show the main menu
        /help - Show this help message
        
        Use the reply keyboard to:
        - Browse 📦 Product Categories
        - Manage 👤 Profile and settings
        - Explore 🌐 Web Development services
        - Access 🛟 Support & FAQ
        - Share 📢 Feedback
        """
        await update.message.reply_text(help_text.strip())
    except Exception as e:
        if settings.debug:
            print(f"Error in help: {e}")
        await update.message.reply_text("Something went wrong. Try again.")