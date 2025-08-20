from telegram import ReplyKeyboardMarkup

# Main Admin Menu Buttons
ADMIN_BUTTONS = {
    "PRODUCTS": "🛒 Product Management",
    "ALL_USERS": "👤 User Management",
    "TRANSACTIONS": "💳 Transactions",
    "ORDERS": "📦 Orders",
    "ANALYTICS": "📊 Analytics",
    "SETTINGS": "⚙️ Settings",
    "BACK_MAIN": "🔙 Back To Main",
}

# Product Management Sub-menu
PRODUCT_BUTTONS = {
    "VIEW_PRODUCTS": "📋 View All Products",
    "ADD_PRODUCT": "➕ Add New Product",
    "EDIT_PRODUCT": "✏️ Edit Product",
    "DELETE_PRODUCT": "🗑️ Delete Product",
    "STOCK_MANAGEMENT": "📦 Manage Stock",
    "BACK_ADMIN": "🔙 Back To Admin",
}

# User Management Sub-menu
USER_BUTTONS = {
    "ALL_USERS": "👥 All Users List",
    "USER_STATS": "📊 User Statistics",
    "SEARCH_USER": "🔍 Search User",
    "ADD_BALANCE": "💰 Add User Balance",
    "BAN_USER": "🚫 Ban/Unban User",
    "BACK_ADMIN": "🔙 Back To Admin",
}

# Transaction Management Sub-menu
TRANSACTION_BUTTONS = {
    "ALL_TRANSACTIONS": "💳 All Transactions",
    "DEPOSITS": "📈 Deposits",
    "PURCHASES": "🛒 Purchases",
    "REFUNDS": "💸 Refunds",
    "PENDING_TRANSACTIONS": "⏳ Pending",
    "BACK_ADMIN": "🔙 Back To Admin",
}

# Order Management Sub-menu
ORDER_BUTTONS = {
    "ALL_ORDERS": "📦 All Orders",
    "PENDING_ORDERS": "⏳ Pending Orders",
    "COMPLETED_ORDERS": "✅ Completed Orders",
    "FAILED_ORDERS": "❌ Failed Orders",
    "ORDER_STATS": "📊 Order Statistics",
    "BACK_ADMIN": "🔙 Back To Admin",
}

# Analytics Sub-menu
ANALYTICS_BUTTONS = {
    "DAILY_STATS": "📅 Daily Statistics",
    "WEEKLY_STATS": "📆 Weekly Statistics",
    "MONTHLY_STATS": "📋 Monthly Statistics",
    "TOP_PRODUCTS": "🏆 Top Products",
    "TOP_USERS": "👑 Top Users",
    "REVENUE_STATS": "💰 Revenue Stats",
    "BACK_ADMIN": "🔙 Back To Admin",
}

def admin_menu():
    keyboard = [
        [ADMIN_BUTTONS["PRODUCTS"], ADMIN_BUTTONS["ALL_USERS"]],
        [ADMIN_BUTTONS["TRANSACTIONS"], ADMIN_BUTTONS["ORDERS"]],
        [ADMIN_BUTTONS["ANALYTICS"], ADMIN_BUTTONS["SETTINGS"]],
        # [ADMIN_BUTTONS["BACK_MAIN"]],
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

def product_management_menu():
    """Product management submenu"""
    keyboard = [
        [PRODUCT_BUTTONS["VIEW_PRODUCTS"], PRODUCT_BUTTONS["ADD_PRODUCT"]],
        [PRODUCT_BUTTONS["EDIT_PRODUCT"], PRODUCT_BUTTONS["DELETE_PRODUCT"]],
        [PRODUCT_BUTTONS["STOCK_MANAGEMENT"]],
        [PRODUCT_BUTTONS["BACK_ADMIN"]],
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )


def user_management_menu():
    """User management submenu"""
    keyboard = [
        [USER_BUTTONS["ALL_USERS"], USER_BUTTONS["USER_STATS"]],
        [USER_BUTTONS["SEARCH_USER"], USER_BUTTONS["ADD_BALANCE"]],
        [USER_BUTTONS["BAN_USER"]],
        [USER_BUTTONS["BACK_ADMIN"]],
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )


def transaction_management_menu():
    """Transaction management submenu"""
    keyboard = [
        [TRANSACTION_BUTTONS["ALL_TRANSACTIONS"], TRANSACTION_BUTTONS["DEPOSITS"]],
        [TRANSACTION_BUTTONS["PURCHASES"], TRANSACTION_BUTTONS["REFUNDS"]],
        [TRANSACTION_BUTTONS["PENDING_TRANSACTIONS"]],
        [TRANSACTION_BUTTONS["BACK_ADMIN"]],
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )


def order_management_menu():
    """Order management submenu"""
    keyboard = [
        [ORDER_BUTTONS["ALL_ORDERS"], ORDER_BUTTONS["PENDING_ORDERS"]],
        [ORDER_BUTTONS["COMPLETED_ORDERS"], ORDER_BUTTONS["FAILED_ORDERS"]],
        [ORDER_BUTTONS["ORDER_STATS"]],
        [ORDER_BUTTONS["BACK_ADMIN"]],
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )


def analytics_menu():
    """Analytics submenu"""
    keyboard = [
        [ANALYTICS_BUTTONS["DAILY_STATS"], ANALYTICS_BUTTONS["WEEKLY_STATS"]],
        [ANALYTICS_BUTTONS["MONTHLY_STATS"], ANALYTICS_BUTTONS["TOP_PRODUCTS"]],
        [ANALYTICS_BUTTONS["TOP_USERS"], ANALYTICS_BUTTONS["REVENUE_STATS"]],
        [ANALYTICS_BUTTONS["BACK_ADMIN"]],
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )