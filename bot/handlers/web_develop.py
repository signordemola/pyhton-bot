from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import CallbackContext

from bot.keyboards.home import back_button


async def show_web_develop(update: Update, context: CallbackContext) -> None:
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    web_text = """
    🌐 Web Development

    Copying web sites, administration.

    Websites from 0 - help with technical specifications, design, 
    development, deployment and customization.

    Improvement of ready-made solutions.

    Prices:
    - Copy + cleaning from scripts and trackers + edits - from $100
    - Development of the site from 0 - from $200
    - Deployment and customization - from $50
    - Refinements - from $50
    """
    await update.message.reply_text(
        web_text.strip()
    )