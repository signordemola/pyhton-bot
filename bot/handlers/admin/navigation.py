from telegram import Update
from telegram.ext import ContextTypes

from bot.handlers.admin.analytics import show_analytics, show_daily_stats, show_weekly_stats, show_monthly_stats, \
    show_top_products, show_top_users, show_revenue_stats
from bot.handlers.admin.orders import show_order_management, view_all_orders, view_pending_orders, \
    view_completed_orders, view_failed_orders, show_order_statistics
from bot.handlers.admin.products import view_all_products, add_product_prompt, edit_product_prompt, \
    delete_product_prompt, manage_stock, show_product_management
from bot.handlers.admin.settings import show_settings
from bot.handlers.admin.transactions import show_transaction_management, view_all_transactions, view_deposits, \
    view_purchases, view_refunds, view_pending_transactions
from bot.handlers.admin.users import show_user_management, view_all_users, search_user_prompt, show_user_statistics, \
    add_balance_prompt, ban_user_prompt
from bot.keyboards.admin import ADMIN_BUTTONS, PRODUCT_BUTTONS, USER_BUTTONS, TRANSACTION_BUTTONS, ORDER_BUTTONS, \
    ANALYTICS_BUTTONS, admin_menu
from bot.keyboards.home import main_menu
from bot.utils.admin_auth import admin_required


@admin_required
async def handle_admin_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return None

    text = update.message.text

    ADMIN_ROUTES = {
        ADMIN_BUTTONS["PRODUCTS"]: show_product_management,
        ADMIN_BUTTONS["ALL_USERS"]: show_user_management,
        ADMIN_BUTTONS["TRANSACTIONS"]: show_transaction_management,
        ADMIN_BUTTONS["ORDERS"]: show_order_management,
        ADMIN_BUTTONS["ANALYTICS"]: show_analytics,
        ADMIN_BUTTONS["SETTINGS"]: show_settings,
        ADMIN_BUTTONS["BACK_MAIN"]: back_to_main_menu,
    }

    PRODUCT_ROUTES = {
        PRODUCT_BUTTONS["VIEW_PRODUCTS"]: view_all_products,
        PRODUCT_BUTTONS["ADD_PRODUCT"]: add_product_prompt,
        PRODUCT_BUTTONS["EDIT_PRODUCT"]: edit_product_prompt,
        PRODUCT_BUTTONS["DELETE_PRODUCT"]: delete_product_prompt,
        PRODUCT_BUTTONS["STOCK_MANAGEMENT"]: manage_stock,
        PRODUCT_BUTTONS["BACK_ADMIN"]: back_to_admin_menu,
    }

    USER_ROUTES = {
        USER_BUTTONS["ALL_USERS"]: view_all_users,
        USER_BUTTONS["USER_STATS"]: show_user_statistics,
        USER_BUTTONS["SEARCH_USER"]: search_user_prompt,
        USER_BUTTONS["ADD_BALANCE"]: add_balance_prompt,
        USER_BUTTONS["BAN_USER"]: ban_user_prompt,
        USER_BUTTONS["BACK_ADMIN"]: back_to_admin_menu,
    }

    TRANSACTION_ROUTES = {
        TRANSACTION_BUTTONS["ALL_TRANSACTIONS"]: view_all_transactions,
        TRANSACTION_BUTTONS["DEPOSITS"]: view_deposits,
        TRANSACTION_BUTTONS["PURCHASES"]: view_purchases,
        TRANSACTION_BUTTONS["REFUNDS"]: view_refunds,
        TRANSACTION_BUTTONS["PENDING_TRANSACTIONS"]: view_pending_transactions,
        TRANSACTION_BUTTONS["BACK_ADMIN"]: back_to_admin_menu,
    }

    ORDER_ROUTES = {
        ORDER_BUTTONS["ALL_ORDERS"]: view_all_orders,
        ORDER_BUTTONS["PENDING_ORDERS"]: view_pending_orders,
        ORDER_BUTTONS["COMPLETED_ORDERS"]: view_completed_orders,
        ORDER_BUTTONS["FAILED_ORDERS"]: view_failed_orders,
        ORDER_BUTTONS["ORDER_STATS"]: show_order_statistics,
        ORDER_BUTTONS["BACK_ADMIN"]: back_to_admin_menu,
    }

    ANALYTICS_ROUTES = {
        ANALYTICS_BUTTONS["DAILY_STATS"]: show_daily_stats,
        ANALYTICS_BUTTONS["WEEKLY_STATS"]: show_weekly_stats,
        ANALYTICS_BUTTONS["MONTHLY_STATS"]: show_monthly_stats,
        ANALYTICS_BUTTONS["TOP_PRODUCTS"]: show_top_products,
        ANALYTICS_BUTTONS["TOP_USERS"]: show_top_users,
        ANALYTICS_BUTTONS["REVENUE_STATS"]: show_revenue_stats,
        ANALYTICS_BUTTONS["BACK_ADMIN"]: back_to_admin_menu,
    }

    ROUTES = {
        **ADMIN_ROUTES,
        **PRODUCT_ROUTES,
        **USER_ROUTES,
        **TRANSACTION_ROUTES,
        **ORDER_ROUTES,
        **ANALYTICS_ROUTES,
    }

    handler = ROUTES.get(text)

    if handler:
        return await handler(update, context)

    return None


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

