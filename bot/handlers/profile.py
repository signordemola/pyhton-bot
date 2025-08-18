from telegram import Update
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ChatAction
from telegram.ext import CallbackContext

from database.models import sql_cursor, User


async def show_profile(update: Update, context: CallbackContext) -> None:
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    user = update.effective_user
    username = user.username or 'Not set'
    user_id = user.id or 'Not set'

    balance = 0.0
    purchases = 0

    with sql_cursor() as session:
        db_user = session.query(User).filter(User.telegram_id == user.id).first()

        if db_user:
            balance = float(db_user.balance)
            purchases = db_user.purchases


    profile_text = f"""
👤 Your Profile

👨‍💼 Username: {username}

🆔 ID: {user_id}

💰 Balance: ${balance:.2f}

🛒 Purchases: {purchases}
    """

    topup_button = InlineKeyboardButton("💸 Top-up balance", callback_data="topup")
    reply_markup = InlineKeyboardMarkup([[topup_button]])
    await update.message.reply_text(
        profile_text.strip(),
        reply_markup=reply_markup
    )