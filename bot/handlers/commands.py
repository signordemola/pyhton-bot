from sqlalchemy import func
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from bot.keyboards.home import main_menu
from config.settings import settings
from database.models import sql_cursor, User


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Star Bot Application"""

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    try:
        user = update.effective_user

        with sql_cursor() as session:
            db_user = session.query(User).filter(User.telegram_id == user.id).first()

            if db_user:
                db_user.username = user.username
                db_user.first_name = user.first_name
                db_user.last_activity = func.now()
            else:
                new_user = User(
                    telegram_id=user.id,
                    username=user.username,
                    first_name=user.first_name,
                    balance=100.0,
                    purchases=0,
                    is_active=True
                )

                session.add(new_user)

        welcome_text = f"""
        🎉 Welcome to Our Bot, {user.first_name}!
        """
        await update.message.reply_text(welcome_text.strip(), reply_markup=main_menu())
    except Exception as e:
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
        print(f"Error in help: {e}")
        await update.message.reply_text("Something went wrong, Try again!")
