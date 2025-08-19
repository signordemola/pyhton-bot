from telegram import Update
from telegram.ext import ContextTypes
from bot.keyboards.menu import MENU_BUTTONS, main_menu
from bot.handlers.feedback import show_feedback, handle_feedback_input
from bot.handlers.products import show_products, handle_product_click
from bot.handlers.profile import show_profile
from bot.handlers.support import show_support
from bot.handlers.web_develop import show_web_develop
import logging

logger = logging.getLogger(__name__)

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all menu interactions and routing"""
    try:
        text = update.message.text

        if context.user_data.get('awaiting_feedback', False):
            if text == MENU_BUTTONS["BACK_MAIN"]:
                context.user_data['awaiting_feedback'] = False
                await back_to_main(update, context)
                return
            await handle_feedback_input(update, context)
            return

        if context.user_data.get('in_product_detail', False):
            if text.startswith("💳 Buy for $"):
                from bot.handlers.products import handle_buy_button
                await handle_buy_button(update, context)
                return
            elif text == "❌ Insufficient Balance":
                await update.message.reply_text(
                    "💳 You don't have enough balance to purchase this item. Please add funds to your account."
                )
                return
            elif text == "💰 Add To Balance":
                from bot.handlers.products import handle_add_balance
                await handle_add_balance(update, context)
                return
            elif text == "🔙 Back to Products":
                context.user_data.pop('current_product', None)
                context.user_data.pop('in_product_detail', None)
                await show_products(update, context)
                return

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
        elif context.user_data.get('in_products', False):
            if text == MENU_BUTTONS["BACK_MAIN"]:
                context.user_data.pop('in_products', None)
                await back_to_main(update, context)
                return

            await handle_product_click(update, context, text)
            return
        elif text == MENU_BUTTONS["BACK_MAIN"]:
            await back_to_main(update, context)
        else:
            await update.message.reply_text(
                "Please use the menu buttons below:",
                reply_markup=main_menu()
            )

    except Exception as e:
        logger.error(f"Error in handle_menu for text '{text}': {e}", exc_info=True)
        await update.message.reply_text(
            "Something went wrong. Try again.",
            reply_markup=main_menu()
        )

async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Return user to main menu and clear state"""

    context.user_data.clear()

    welcome_text = f"""
🏠
    """
    await update.message.reply_text(
        welcome_text.strip(),
        reply_markup=main_menu()
    )