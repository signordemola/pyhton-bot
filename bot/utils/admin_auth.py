import logging
from typing import Optional

from telegram import Update

from bot.keyboards.home import main_menu
from config.settings import settings

logger = logging.getLogger(__name__)

def is_user_admin(telegram_id: int, username: Optional[str] = None) -> bool:
    """Check if user is admin"""

    try:
        if telegram_id not in settings.ADMIN_IDS:
            logger.warning("User is not admin")
            return False

        if settings.ADMIN_USERNAME and username:
            clean_username = username.lstrip('@').lower()
            admin_username = settings.ADMIN_USERNAME.lstrip('@').lower()

            if clean_username != admin_username:
                logger.warning("User is not admin and username doesn't match")
                return False

        logger.info(f"Admin authentication successful for {telegram_id}")
        return True

    except Exception as e:
        logger.error(f"Failed to authenticate with telegram ID {telegram_id}: {e}")
        return False



def admin_required(func):
    """Decorator to require admin authentication for handler functions"""

    async def wrapper(update: Update, context):
        user = update.effective_user
        if not user or not is_user_admin(telegram_id=user.id, username=user.username):
            await update.message.reply_text(
                "Redirecting to main menu...",
                reply_markup=main_menu()
            )
            return None

        return await func(update, context)

    return wrapper

