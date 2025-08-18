from telegram import ReplyKeyboardMarkup

PRODUCT_BUTTONS = {
    "SAKURA": "sakura.ad.JP",
    "PRIVATEEMAIL": "privateemail.com",
    "REGISTER": "register.it",
    "AWS": "AWS Workmail",
    "BIZMAIL": "bizmail.yahoo",
    "BACK_MAIN": "🔙 Back"
}


def products_keyboard():
    keyboard = [
        [PRODUCT_BUTTONS["SAKURA"], PRODUCT_BUTTONS["PRIVATEEMAIL"]],
        [PRODUCT_BUTTONS["REGISTER"], PRODUCT_BUTTONS["AWS"]],
        [PRODUCT_BUTTONS["BIZMAIL"]],
        [PRODUCT_BUTTONS["BACK_MAIN"]]
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )