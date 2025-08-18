from datetime import datetime

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import CallbackContext

from bot.keyboards.menu import back_button
from config.settings import settings


async def show_feedback(update: Update, context: CallbackContext) -> None:
    """Show feedback form when FEEDBACK menu button is pressed"""
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    context.user_data['awaiting_feedback'] = True

    feedback_text = """
📝 Use this form to send us your opinion about the service.
For example, what new products/functions you would like to see in the bot.

Write your suggestion:
    """
    await update.message.reply_text(
        feedback_text.strip(),
        reply_markup=back_button(),
        reply_to_message_id=update.message.message_id
    )


async def handle_feedback_input(update: Update, context: CallbackContext) -> None:
    """Handle feedback message and send to admins"""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    user_feedback = update.message.text
    username = update.effective_user.username or "No username"
    first_name = update.effective_user.first_name or "Unknown"

    admin_message = f"""
    🎯 **New Feedback**

    👤 **From:**
    • {first_name} (@{username})
    • User ID: `{user_id}`
    • Chat ID: `{chat_id}`

    💬 **Message:**
    {user_feedback}

    📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """

    for admin_id in settings.ADMIN_IDS:
        try:
            await context.bot.send_message(
                chat_id=admin_id,
                text=admin_message.strip(),
                parse_mode='Markdown'
            )
        except Exception as e:
            print(f"Failed to send feedback to admin {admin_id}: {e}")

    context.user_data['awaiting_feedback'] = False

    await update.message.reply_text("✅ Thank you for your feedback! It has been sent to the admin.")

