from telegram import Update
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ChatAction
from telegram.ext import CallbackContext


async def show_profile(update: Update, context: CallbackContext) -> None:
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    user = update.effective_user
    username = user.username or 'Not set'
    user_id = user.id or 'Not set'

    profile_text = f"""
    👤 Your Profile

    👨‍💼 Username: {username}

    🆔 ID: {user_id}

    💰 Balance: $0

    🛒 Purchases: 0
    """

    topup_button = InlineKeyboardButton("💸 Top-up balance", callback_data="topup")
    reply_markup = InlineKeyboardMarkup([[topup_button]])
    await update.message.reply_text(
        profile_text.strip(),
        reply_markup=reply_markup
    )