from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from sqlalchemy import func

from bot.keyboards.admin import (
    ADMIN_BUTTONS, PRODUCT_BUTTONS, USER_BUTTONS, TRANSACTION_BUTTONS,
    ORDER_BUTTONS, ANALYTICS_BUTTONS, admin_menu, product_management_menu,
    user_management_menu, transaction_management_menu, order_management_menu,
    analytics_menu
)
from bot.keyboards.home import main_menu
from bot.utils.admin_auth import admin_required
from database.models import sql_cursor, User, Product, Order, Transaction, OrderStatus, TransactionStatus


@admin_required
async def handle_admin_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin menu navigation"""

    text = update.message.text

    # Main admin menu navigation
    if text == ADMIN_BUTTONS["PRODUCTS"]:
        await show_product_management(update, context)
    elif text == ADMIN_BUTTONS["ALL_USERS"]:
        await show_user_management(update, context)
    elif text == ADMIN_BUTTONS["TRANSACTIONS"]:
        await show_transaction_management(update, context)
    elif text == ADMIN_BUTTONS["ORDERS"]:
        await show_order_management(update, context)
    elif text == ADMIN_BUTTONS["ANALYTICS"]:
        await show_analytics(update, context)
    elif text == ADMIN_BUTTONS["SETTINGS"]:
        await show_settings(update, context)
    elif text == ADMIN_BUTTONS["BACK_MAIN"]:
        await back_to_main_menu(update, context)

    # Product management navigation
    elif text == PRODUCT_BUTTONS["VIEW_PRODUCTS"]:
        await view_all_products(update, context)
    elif text == PRODUCT_BUTTONS["ADD_PRODUCT"]:
        await add_product_prompt(update, context)
    elif text == PRODUCT_BUTTONS["EDIT_PRODUCT"]:
        await edit_product_prompt(update, context)
    elif text == PRODUCT_BUTTONS["DELETE_PRODUCT"]:
        await delete_product_prompt(update, context)
    elif text == PRODUCT_BUTTONS["STOCK_MANAGEMENT"]:
        await manage_stock(update, context)
    elif text == PRODUCT_BUTTONS["BACK_ADMIN"]:
        await back_to_admin_menu(update, context)

    # User management navigation
    elif text == USER_BUTTONS["ALL_USERS"]:
        await view_all_users(update, context)
    elif text == USER_BUTTONS["USER_STATS"]:
        await show_user_statistics(update, context)
    elif text == USER_BUTTONS["SEARCH_USER"]:
        await search_user_prompt(update, context)
    elif text == USER_BUTTONS["ADD_BALANCE"]:
        await add_balance_prompt(update, context)
    elif text == USER_BUTTONS["BAN_USER"]:
        await ban_user_prompt(update, context)
    elif text == USER_BUTTONS["BACK_ADMIN"]:
        await back_to_admin_menu(update, context)

    # Transaction management navigation
    elif text == TRANSACTION_BUTTONS["ALL_TRANSACTIONS"]:
        await view_all_transactions(update, context)
    elif text == TRANSACTION_BUTTONS["DEPOSITS"]:
        await view_deposits(update, context)
    elif text == TRANSACTION_BUTTONS["PURCHASES"]:
        await view_purchases(update, context)
    elif text == TRANSACTION_BUTTONS["REFUNDS"]:
        await view_refunds(update, context)
    elif text == TRANSACTION_BUTTONS["PENDING_TRANSACTIONS"]:
        await view_pending_transactions(update, context)
    elif text == TRANSACTION_BUTTONS["BACK_ADMIN"]:
        await back_to_admin_menu(update, context)

    # Order management navigation
    elif text == ORDER_BUTTONS["ALL_ORDERS"]:
        await view_all_orders(update, context)
    elif text == ORDER_BUTTONS["PENDING_ORDERS"]:
        await view_pending_orders(update, context)
    elif text == ORDER_BUTTONS["COMPLETED_ORDERS"]:
        await view_completed_orders(update, context)
    elif text == ORDER_BUTTONS["FAILED_ORDERS"]:
        await view_failed_orders(update, context)
    elif text == ORDER_BUTTONS["ORDER_STATS"]:
        await show_order_statistics(update, context)
    elif text == ORDER_BUTTONS["BACK_ADMIN"]:
        await back_to_admin_menu(update, context)

    # Analytics navigation
    elif text == ANALYTICS_BUTTONS["DAILY_STATS"]:
        await show_daily_stats(update, context)
    elif text == ANALYTICS_BUTTONS["WEEKLY_STATS"]:
        await show_weekly_stats(update, context)
    elif text == ANALYTICS_BUTTONS["MONTHLY_STATS"]:
        await show_monthly_stats(update, context)
    elif text == ANALYTICS_BUTTONS["TOP_PRODUCTS"]:
        await show_top_products(update, context)
    elif text == ANALYTICS_BUTTONS["TOP_USERS"]:
        await show_top_users(update, context)
    elif text == ANALYTICS_BUTTONS["REVENUE_STATS"]:
        await show_revenue_stats(update, context)
    elif text == ANALYTICS_BUTTONS["BACK_ADMIN"]:
        await back_to_admin_menu(update, context)


# Main Menu Functions
@admin_required
async def show_product_management(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show product management menu"""

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    with sql_cursor() as session:
        total_products = session.query(Product).count()
        active_products = session.query(Product).filter(Product.is_active == True).count()
        out_of_stock = session.query(Product).filter(Product.stock <= 0).count()

    text = f"""🛒 <b>Product Management</b>

📊 <b>Quick Stats:</b>
• Total Products: <code>{total_products}</code>
• Active Products: <code>{active_products}</code>
• Out of Stock: <code>{out_of_stock}</code>

Choose an action from the menu below:"""

    await update.message.reply_text(
        text,
        parse_mode='HTML',
        reply_markup=product_management_menu()
    )


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
async def show_analytics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show analytics menu"""

    text = """📊 <b>Analytics Dashboard</b>

📈 View detailed statistics and insights about your bot's performance.

Choose an analytics option from the menu below:"""

    await update.message.reply_text(
        text,
        parse_mode='HTML',
        reply_markup=analytics_menu()
    )


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


# Detailed View Functions
@admin_required
async def view_all_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """View all products"""

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    with sql_cursor() as session:
        products = session.query(Product).order_by(Product.created_at.desc()).limit(10).all()

    if not products:
        text = "🛒 <b>All Products</b>\n\n❌ No products found."
    else:
        text = "🛒 <b>All Products</b> (Last 10)\n\n"

        for product in products:
            status = "✅" if product.is_active else "❌"
            stock_status = "📦" if product.stock > 0 else "🚫"

            text += f"{status} <b>{product.name}</b>\n"
            text += f"💰 Price: <code>${product.price}</code>\n"
            text += f"{stock_status} Stock: <code>{product.stock}</code>\n\n"

    await update.message.reply_text(
        text,
        parse_mode='HTML',
        reply_markup=product_management_menu()
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


# Placeholder functions for missing handlers
@admin_required
async def add_product_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add product prompt - placeholder"""
    text = "➕ <b>Add New Product</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=product_management_menu())


@admin_required
async def edit_product_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Edit product prompt - placeholder"""
    text = "✏️ <b>Edit Product</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=product_management_menu())


@admin_required
async def delete_product_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete product prompt - placeholder"""
    text = "🗑️ <b>Delete Product</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=product_management_menu())


@admin_required
async def manage_stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manage stock - placeholder"""
    text = "📦 <b>Manage Stock</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=product_management_menu())


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


@admin_required
async def show_daily_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show daily statistics"""
    text = "📅 <b>Daily Statistics</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=analytics_menu())


@admin_required
async def show_weekly_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show weekly statistics"""
    text = "📆 <b>Weekly Statistics</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=analytics_menu())


@admin_required
async def show_monthly_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show monthly statistics"""
    text = "📋 <b>Monthly Statistics</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=analytics_menu())


@admin_required
async def show_top_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show top products"""
    text = "🏆 <b>Top Products</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=analytics_menu())


@admin_required
async def show_top_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show top users"""
    text = "👑 <b>Top Users</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=analytics_menu())


@admin_required
async def show_revenue_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show revenue statistics"""
    text = "💰 <b>Revenue Statistics</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=analytics_menu())


# Navigation Functions
async def back_to_admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Return to main admin menu"""

    text = "🔐 <b>Admin Panel</b>\n\nReturned to main admin menu."

    await update.message.reply_text(
        text,
        parse_mode='HTML',
        reply_markup=admin_menu()
    )


async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Return to main bot menu"""

    context.user_data.clear()

    text = "🏠 <b>Main Menu</b>\n\nExited admin panel."

    await update.message.reply_text(
        text,
        parse_mode='HTML',
        reply_markup=main_menu()
    )