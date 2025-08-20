from telegram import ReplyKeyboardMarkup

MENU_BUTTONS = {
    "PRODUCTS": "🛒 Product categories",
    "PROFILE": "👤 Profile",
    "WEB_DEVELOP": "🌐 Web development",
    "SUPPORT": "💬 Support / FAQ",
    "FEEDBACK": "📢 Feedback",
    "BACK_MAIN": "🔙 Back",
}

def main_menu():
    keyboard = [
        [MENU_BUTTONS["PRODUCTS"], MENU_BUTTONS["PROFILE"]],
        [MENU_BUTTONS["WEB_DEVELOP"]],
        [MENU_BUTTONS["SUPPORT"], MENU_BUTTONS["FEEDBACK"]],
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

def back_button():
    keyboard = [[MENU_BUTTONS["BACK_MAIN"]]]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )