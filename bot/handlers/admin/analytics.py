from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards.admin import analytics_menu
from bot.utils.admin_auth import admin_required


@admin_required
async def show_analytics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show analytics menu"""

    text = """📊 <b>Analytics Dashboard</b>

📈 View detailed statistics and insights about your bot's performance.

Choose an analytics option from the menu below:"""

    await update.message.reply_text(
        text,
        parse_mode='HTML',
        reply_markup=analytics_menu()
    )

@admin_required
async def show_daily_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show daily statistics"""
    text = "📅 <b>Daily Statistics</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=analytics_menu())


@admin_required
async def show_weekly_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show weekly statistics"""
    text = "📆 <b>Weekly Statistics</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=analytics_menu())


@admin_required
async def show_monthly_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show monthly statistics"""
    text = "📋 <b>Monthly Statistics</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=analytics_menu())


@admin_required
async def show_top_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show top products"""
    text = "🏆 <b>Top Products</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=analytics_menu())


@admin_required
async def show_top_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show top users"""
    text = "👑 <b>Top Users</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=analytics_menu())


@admin_required
async def show_revenue_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show revenue statistics"""
    text = "💰 <b>Revenue Statistics</b>\n\n<i>Feature coming soon...</i>"
    await update.message.reply_text(text, parse_mode='HTML', reply_markup=analytics_menu())




