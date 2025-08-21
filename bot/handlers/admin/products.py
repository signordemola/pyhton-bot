from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from bot.keyboards.admin import product_management_menu
from bot.utils.admin_auth import admin_required
from database.models import sql_cursor, Product


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
