from telegram.ext import ContextTypes
from telegram import Update
from telegram.constants import ChatAction

from bot.keyboards.admin import admin_menu


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin Command Profile"""

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    try:
        user = update.effective_user

        print(f"\n\n\nAdmin User: {user}")

        welcome_text = f"""
        🎉 Welcome Admin, {user.first_name}!
        """
        await update.message.reply_text(welcome_text.strip(), reply_markup=admin_menu())
    except Exception as e:
        print(f"Error in admin: {e}")
        await update.message.reply_text("Something went wrong, Try again!")