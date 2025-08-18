from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards.menu import MENU_BUTTONS, main_menu
from bot.handlers.feedback import show_feedback
from bot.handlers.products import show_products
from bot.handlers.profile import show_profile
from bot.handlers.support import show_support
from bot.handlers.web_develop import show_web_develop
import logging

logger = logging.getLogger(__name__)

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        if text == MENU_BUTTONS["PRODUCTS"]:
            await show_products(update, context)
        elif text == MENU_BUTTONS["PROFILE"]:
            await show_profile(update, context)
        elif text == MENU_BUTTONS["WEB_DEVELOP"]:
            await show_web_develop(update, context)
        elif text == MENU_BUTTONS["SUPPORT"]:
            await show_support(update, context)
        elif text == MENU_BUTTONS["FEEDBACK"]:
            await show_feedback(update, context)
        elif text == MENU_BUTTONS["BACK_MAIN"]:
            await back_to_main(update)
    except Exception as e:
        logger.error(f"Error in handle_menu for text '{text}': {e}", exc_info=True)
        await update.message.reply_text("Something went wrong. Try again.", reply_markup=main_menu())

async def back_to_main(update: Update):
    welcome_text = f"""
🏠
    """
    await update.message.reply_text(
        welcome_text.strip(),
        reply_markup=main_menu()
    )