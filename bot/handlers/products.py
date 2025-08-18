from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import CallbackContext

from bot.keyboards.products import products_keyboard


async def show_products(update: Update, context: CallbackContext) -> None:
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    products_text = """
📁 These are all available product categories:
    """

    await update.message.reply_text(
        products_text.strip(),
        reply_markup=products_keyboard()
    )