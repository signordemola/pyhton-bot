from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatAction
from telegram.ext import CallbackContext

from config.settings import settings


async def show_support(update: Update, context: CallbackContext) -> None:
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    support_text = """
**📋 Frequently Asked Questions:**

**Q: How do I make a payment?**
A: We accept crypto payments. Check Payment Guide for details.

**Q: How long does delivery take?**
A: Digital products are delivered instantly after payment confirmation.

**Q: Can I get a refund?**
A: Refunds are processed within 24 hours for valid cases.

**Q: My product isn't working, what do I do?**
A: Contact support immediately with your order details.

**Q: How do I check my order status?**
A: Use the "My Orders" section in your Profile.

**Q: Is my payment secure?**
A: Yes, we use encrypted payment processing for all transactions.

────────────────────────

**💬 Need more help?**
Contact our admin for direct support:
    """

    contact_button = InlineKeyboardButton("💬 Contact Admin", url=f"https://t.me/{settings.ADMIN_USERNAME}")
    reply_markup = InlineKeyboardMarkup([[contact_button]])
    await update.message.reply_text(
        support_text.strip(),
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )