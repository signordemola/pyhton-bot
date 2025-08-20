from telegram import Update
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ChatAction
from telegram.ext import CallbackContext

from database.models import sql_cursor, User


async def show_profile(update: Update, context: CallbackContext) -> None:
    """Display user profile information"""

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    user = update.effective_user
    username = user.username or 'Not set'
    user_id = user.id or 'Not set'



    with sql_cursor() as session:
        db_user = session.query(User).filter(User.telegram_id == user.id).first()

        if db_user:
            balance = float(db_user.balance)
            purchases = db_user.purchases
        else:
            balance = 0.0
            purchases = 0


    profile_text = f"""
👤 Your Profile

👨‍💼 Username: {username}

🆔 ID: {user_id}

💰 Balance: ${balance:.2f}

🛒 Purchases: {purchases}
    """

    add_balance_button = InlineKeyboardButton("💸 Add To Balance", callback_data="add_balance")
    reply_markup = InlineKeyboardMarkup([[add_balance_button]])

    await update.message.reply_text(
        profile_text.strip(),
        reply_markup=reply_markup
    )

async def handle_profile_add_balance(update: Update, context: CallbackContext) -> None:
    """Handle add balance button click from profile (InlineKeyboard)"""

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    query = update.callback_query
    await query.answer("💰 Contact admin to add balance!")