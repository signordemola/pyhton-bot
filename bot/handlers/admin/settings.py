from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards.admin import admin_menu
from bot.utils.admin_auth import admin_required


@admin_required
async def show_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show settings"""

    text = """⚙️ <b>Settings</b>

🔧 Bot configuration and system settings.

<i>Settings features coming soon...</i>"""

    await update.message.reply_text(
        text,
        parse_mode='HTML',
        reply_markup=admin_menu()
    )