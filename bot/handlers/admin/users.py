from sqlalchemy import func
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from bot.keyboards.admin import user_management_menu
from bot.utils.admin_auth import admin_required
from database.models import sql_cursor, User


@admin_required
async def show_user_management(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user management menu"""

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    with sql_cursor() as session:
        total_users = session.query(User).count()
        active_users = session.query(User).filter(User.is_active == True).count()
        users_with_purchases = session.query(User).filter(User.purchases > 0).count()
        total_balance = session.query(func.sum(User.balance)).scalar() or 0

    text = f"""👤 <b>User Management</b>

📊 <b>Quick Stats:</b>
• Total Users: <code>{total_users}</code>
• Active Users: <code>{active_users}</code>
• Users with Purchases: <code>{users_with_purchases}</code>
• Total User Balance: <code>${total_balance}</code>

Choose an action from the menu below:"""

    await update.message.reply_text(
        text,
        parse_mode='HTML',
        reply_markup=user_management_menu()
    )

@admin_required
async def view_all_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View all users"""

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    with sql_cursor() as session:
        users = session.query(User).order_by(User.created_at.desc()).limit(10).all()

        if not users:
            text = "👤 <b>All Users</b>\n\n❌ No users found."
        else:
            text = "👤 <b>All Users</b> (Last 10)\n\n"

            for user in users:
                status = "✅" if user.is_active else "❌"

                text += f"{status} <b>{user.first_name or 'N/A'}</b>\n"
                text += f"👨‍💼 @{user.username or 'N/A'}\n"
                text += f"🆔 ID: <code>{user.telegram_id}</code>\n"
                text += f"💰 Balance: <code>${user.balance}</code>\n"
                text += f"🛒 Purchases: <code>{user.purchases}</code>\n\n"

    await update.message.reply_text(
        text,
        parse_mode='HTML',
        reply_markup=user_management_menu()
    )


@admin_required
async def show_user_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user statistics - placeholder"""
    text = "📊 <b>User Statistics</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=user_management_menu())


@admin_required
async def search_user_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Search user prompt - placeholder"""
    text = "🔍 <b>Search User</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=user_management_menu())


@admin_required
async def add_balance_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add balance prompt - placeholder"""
    text = "💰 <b>Add User Balance</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=user_management_menu())

@admin_required
async def ban_user_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ban user prompt - placeholder"""
    text = "🚫 <b>Ban/Unban User</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=user_management_menu())




