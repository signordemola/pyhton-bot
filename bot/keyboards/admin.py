from telegram import ReplyKeyboardMarkup

ADMIN_BUTTONS = {
    "PRODUCTS": "🛒 Product categories",
    "ALL_USERS": "👤 All Users",
    "WEB_DEVELOP": "🌐 Web development",
    "SUPPORT": "💬 Support / FAQ",
    "FEEDBACK": "📢 Feedback",
    "BACK_MAIN": "🔙 Back",
}

def admin_menu():
    keyboard = [
        [ADMIN_BUTTONS["PRODUCTS"], ADMIN_BUTTONS["ALL_USERS"]],
        [ADMIN_BUTTONS["WEB_DEVELOP"]],
        [ADMIN_BUTTONS["SUPPORT"], ADMIN_BUTTONS["FEEDBACK"]],
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

