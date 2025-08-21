from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from bot.keyboards.admin import order_management_menu
from bot.utils.admin_auth import admin_required
from database.models import OrderStatus, Order, sql_cursor


@admin_required
async def show_order_management(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show order management menu"""

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    with sql_cursor() as session:
        total_orders = session.query(Order).count()
        completed_orders = session.query(Order).filter(Order.status == OrderStatus.COMPLETED).count()
        pending_orders = session.query(Order).filter(Order.status == OrderStatus.PENDING).count()
        failed_orders = session.query(Order).filter(Order.status == OrderStatus.FAILED).count()

    text = f"""📦 <b>Order Management</b>

📊 <b>Quick Stats:</b>
• Total Orders: <code>{total_orders}</code>
• Completed: <code>{completed_orders}</code>
• Pending: <code>{pending_orders}</code>
• Failed: <code>{failed_orders}</code>

Choose an action from the menu below:"""

    await update.message.reply_text(
        text,
        parse_mode='HTML',
        reply_markup=order_management_menu()
    )


@admin_required
async def view_all_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View all orders"""

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    with sql_cursor() as session:
        orders = session.query(Order).order_by(Order.created_at.desc()).limit(10).all()

    if not orders:
        text = "📦 <b>All Orders</b>\n\n❌ No orders found."
    else:
        text = "📦 <b>All Orders</b> (Last 10)\n\n"

        for order in orders:
            status_icon = {
                "completed": "✅",
                "pending": "⏳",
                "failed": "❌",
                "cancelled": "🚫"
            }.get(order.status.value, "❓")

            text += f"📦 <b>Order #{order.id}</b> {status_icon}\n"
            text += f"💰 Amount: <code>${order.total_amount}</code>\n"
            text += f"🔢 Quantity: <code>{order.quantity}</code>\n"
            text += f"🆔 User ID: <code>{order.user_id}</code>\n"
            text += f"📅 {order.created_at.strftime('%Y-%m-%d %H:%M')}\n\n"

    await update.message.reply_text(
        text,
        parse_mode='HTML',
        reply_markup=order_management_menu()
    )

@admin_required
async def view_pending_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View pending orders"""
    text = "⏳ <b>Pending Orders</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=order_management_menu())


@admin_required
async def view_completed_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View completed orders"""
    text = "✅ <b>Completed Orders</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=order_management_menu())


@admin_required
async def view_failed_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View failed orders"""
    text = "❌ <b>Failed Orders</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=order_management_menu())


@admin_required
async def show_order_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show order statistics"""
    text = "📊 <b>Order Statistics</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=order_management_menu())





