from sqlalchemy import func
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from bot.keyboards.admin import transaction_management_menu
from bot.utils.admin_auth import admin_required
from database.models import sql_cursor, Transaction, TransactionStatus


@admin_required
async def show_transaction_management(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show transaction management menu"""

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    with sql_cursor() as session:
        total_transactions = session.query(Transaction).count()
        completed_transactions = session.query(Transaction).filter(
            Transaction.status == TransactionStatus.COMPLETED).count()
        pending_transactions = session.query(Transaction).filter(
            Transaction.status == TransactionStatus.PENDING).count()
        total_amount = session.query(func.sum(Transaction.amount)).filter(
            Transaction.status == TransactionStatus.COMPLETED).scalar() or 0

    text = f"""💳 <b>Transaction Management</b>

📊 <b>Quick Stats:</b>
• Total Transactions: <code>{total_transactions}</code>
• Completed: <code>{completed_transactions}</code>
• Pending: <code>{pending_transactions}</code>
• Total Amount: <code>${total_amount}</code>

Choose an action from the menu below:"""

    await update.message.reply_text(
        text,
        parse_mode='HTML',
        reply_markup=transaction_management_menu()
    )


@admin_required
async def view_all_transactions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View all transactions"""

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    with sql_cursor() as session:
        transactions = session.query(Transaction).order_by(Transaction.created_at.desc()).limit(10).all()

    if not transactions:
        text = "💳 <b>All Transactions</b>\n\n❌ No transactions found."
    else:
        text = "💳 <b>All Transactions</b> (Last 10)\n\n"

        for trans in transactions:
            type_icon = {"deposit": "📈", "purchase": "🛒", "refund": "💸"}.get(trans.transaction_type.value, "💳")
            status_icon = {"completed": "✅", "pending": "⏳", "failed": "❌"}.get(trans.status.value, "❓")

            text += f"{type_icon} <b>{trans.transaction_type.value.title()}</b> {status_icon}\n"
            text += f"💰 Amount: <code>${trans.amount}</code>\n"
            text += f"🆔 User ID: <code>{trans.user_id}</code>\n"
            text += f"📅 {trans.created_at.strftime('%Y-%m-%d %H:%M')}\n\n"

    await update.message.reply_text(
        text,
        parse_mode='HTML',
        reply_markup=transaction_management_menu()
    )

@admin_required
async def view_deposits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View deposits"""
    text = "📈 <b>Deposits</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=transaction_management_menu())


@admin_required
async def view_purchases(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View purchases"""
    text = "🛒 <b>Purchases</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=transaction_management_menu())


@admin_required
async def view_refunds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View refunds"""
    text = "💸 <b>Refunds</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=transaction_management_menu())


@admin_required
async def view_pending_transactions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View pending transactions"""
    text = "⏳ <b>Pending Transactions</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=transaction_management_menu())




