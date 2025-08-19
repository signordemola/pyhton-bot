from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from bot.keyboards.menu import MENU_BUTTONS
from database.models import Product, sql_cursor, User


def products_keyboard():
    """Create keyboard with all available products"""

    with sql_cursor() as session:
        products = session.query(Product).filter(
            Product.is_active == True,
            Product.stock > 0
        ).all()

        product_names = [product.name for product in products]

    keyboard = []
    row = []

    for product_name in product_names:
        row.append(product_name)

        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    keyboard.append([MENU_BUTTONS["BACK_MAIN"]])

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )


def create_product_detail_keyboard(product_data: dict, user_balance: float) -> ReplyKeyboardMarkup:
    """Create keyboard for product details using ReplyKeyboardMarkup"""
    keyboard = []

    if user_balance >= product_data['price'] and product_data['stock'] > 0:
        keyboard.append([f"💳 Buy for ${product_data['price']}", "💰 Add To Balance"])
    else:
        keyboard.append(["❌ Insufficient Balance", "💰 Add To Balance"])

    keyboard.append(["🔙 Back to Products"])

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )