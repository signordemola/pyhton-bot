from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import CallbackContext

from bot.keyboards.menu import back_button

async def show_feedback(update: Update, context: CallbackContext) -> None:
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    feedback_text = """
📝 Use this form to send us your opinion about the service.
For example, what new products/functions you would like to see in the bot.

Write your suggestion:
    """
    await update.message.reply_text(
        feedback_text.strip(),
        reply_markup=back_button()
    )