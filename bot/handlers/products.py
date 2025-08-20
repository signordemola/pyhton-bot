from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes
from sqlalchemy import func

from bot.keyboards.products import products_keyboard, create_product_detail_keyboard
from bot.keyboards.home import main_menu
from database.models import sql_cursor, Product, User, Order, Transaction, OrderStatus, TransactionType, TransactionStatus


async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show all products"""

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    with sql_cursor() as session:
        products_count = session.query(Product).filter(
            Product.is_active == True,
            Product.stock > 0
        ).count()

    if products_count == 0:
        await update.message.reply_text(
            "🚫 No products available right now.",
            reply_markup=main_menu()
        )
        return

    await update.message.reply_text(
        "📁 These are all available product categories:",
        reply_markup=products_keyboard()
    )
    context.user_data['in_products'] = True


async def handle_product_click(update: Update, context: ContextTypes.DEFAULT_TYPE, product_name: str):
    """Handle when user clicks on a product name"""

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    with sql_cursor() as session:
        product = session.query(Product).filter(
            Product.name == product_name,
            Product.is_active == True
        ).first()

        user = session.query(User).filter(
            User.telegram_id == update.effective_user.id
        ).first()

        if not product:
            await update.message.reply_text(
                "🚫 Product not found.",
                reply_markup=products_keyboard()
            )
            return

        product_data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock
        }

        user_balance = user.balance

        product_text = f"""
    🛍️ <b>{product_data['name']}</b>

    📝 {product_data['description'] or 'No description'}

    💰 Price: <code>${product_data['price']}</code>
    
    📦 Stock: <code>{product_data['stock']}</code>
    
    💳 Your balance: <code>${user_balance}</code>"""

    context.user_data['current_product'] = product_data
    context.user_data['in_product_detail'] = True

    keyboard = create_product_detail_keyboard(product_data, user_balance)

    await update.message.reply_text(
        product_text,
        parse_mode=ParseMode.HTML,
        reply_markup=keyboard
    )


async def handle_buy_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process purchase when user clicks Buy button"""
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )

    product_data = context.user_data.get('current_product')
    if not product_data:
        await update.message.reply_text(
            "❌ Error occurred. Please select a product again.",
            reply_markup=products_keyboard()
        )
        return

    with sql_cursor() as session:
        product = session.query(Product).filter(Product.id == product_data['id']).first()
        user = session.query(User).filter(User.telegram_id == update.effective_user.id).first()

        if not product or not user:
            await update.message.reply_text("❌ Error occurred. Try again.")
            return

        if user.balance < product.price:
            await update.message.reply_text(
                "💳 Insufficient balance. Please add funds to your account."
            )
            return

        if product.stock <= 0:
            await update.message.reply_text("📦 Product is out of stock.")
            return

        order = Order(
            user_id=user.id,
            product_id=product.id,
            quantity=1,
            total_amount=product.price,
            status=OrderStatus.COMPLETED,
            payment_method="balance",
            completed_at=func.now()
        )
        session.add(order)
        session.flush()

        # Update user and product
        user.balance -= product.price
        user.purchases += 1
        product.stock -= 1

        # Create transaction
        transaction = Transaction(
            user_id=user.id,
            amount=product.price,
            transaction_type=TransactionType.PURCHASE,
            status=TransactionStatus.COMPLETED,
            payment_method="balance"
        )
        session.add(transaction)
        session.commit()

        success_text = f"""
✅ <b>Purchase Successful!</b>

🛍️ Product: <b>{product.name}</b>

💰 Paid: <code>${product.price}</code>

🆔 Order ID: <code>{order.id}</code>

💳 New Balance: <code>${user.balance}</code>

Thank you! 🎉"""

        context.user_data.pop('current_product', None)
        context.user_data.pop('in_product_detail', None)

        await update.message.reply_text(
            success_text,
            parse_mode=ParseMode.HTML,
            reply_markup=products_keyboard()
        )


async def handle_add_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle add balance button click"""
    await update.message.reply_text("💰 Contact admin to add balance!")