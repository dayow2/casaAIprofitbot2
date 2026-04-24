from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# REPLACE THIS WITH YOUR ACTUAL TOKEN FROM BOTFATHER
YOUR_TOKEN = "7234567890:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw"

# Track if the bot is trading (simple state)
is_trading = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with 4 buttons"""
    keyboard = [
        [InlineKeyboardButton("▶️ START TRADING", callback_data='start_trading')],
        [InlineKeyboardButton("📋 SHOW ORDERS", callback_data='show_orders')],
        [InlineKeyboardButton("💰 TAKE PROFIT", callback_data='take_profit')],
        [InlineKeyboardButton("⏹️ STOP TRADING", callback_data='stop_trading')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🤖 *Trading Bot Ready*\n\n"
        "Use the buttons below to control your bot:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button clicks"""
    query = update.callback_query
    await query.answer()  # Acknowledge the button click
    
    global is_trading
    
    if query.data == 'start_trading':
        if not is_trading:
            is_trading = True
            await query.edit_message_text(
                "✅ *Trading Started!*\n\n"
                "Monitoring price at $10.00\n"
                "Will buy at $10.00 and sell at $10.50\n\n"
                "⚠️ This is a demo - no real trades yet",
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text(
                "⚠️ Trading is already running!\n\n"
                "Use STOP TRADING to stop first.",
                parse_mode='Markdown'
            )
    
    elif query.data == 'show_orders':
        await query.edit_message_text(
            "📋 *Current Orders*\n\n"
            "No active orders (demo mode)\n\n"
            "When live, this will show:\n"
            "• Buy: 100 DOGE @ $10.00\n"
            "• Take Profit: $10.50\n"
            "• Current P/L: $0.00",
            parse_mode='Markdown'
        )
    
    elif query.data == 'take_profit':
        if is_trading:
            await query.edit_message_text(
                "💰 *Take Profit Executed!*\n\n"
                "Would have sold at $10.50\n"
                "Profit: $50.00\n\n"
                "⚠️ Demo mode - no real trade occurred",
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text(
                "❌ No active trades to close.\n\n"
                "Start trading first with START TRADING button.",
                parse_mode='Markdown'
            )
    
    elif query.data == 'stop_trading':
        if is_trading:
            is_trading = False
            await query.edit_message_text(
                "⏹️ *Trading Stopped*\n\n"
                "Price monitoring is OFF\n"
                "No new orders will be placed\n\n"
                "Click START TRADING to resume",
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text(
                "⚠️ Trading is already stopped!\n\n"
                "Click START TRADING to begin.",
                parse_mode='Markdown'
            )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send help message"""
    await update.message.reply_text(
        "📖 *How to use this bot:*\n\n"
        "1. Send /start to see the buttons\n"
        "2. Click START TRADING to begin\n"
        "3. Click SHOW ORDERS to see positions\n"
        "4. Click TAKE PROFIT to close winning trades\n"
        "5. Click STOP TRADING to pause\n\n"
        "*Commands:*\n"
        "/start - Show trading panel\n"
        "/help - Show this message",
        parse_mode='Markdown'
    )

def main():
    """Start the bot"""
    print("🤖 Bot is starting...")
    
    # Create the application
    app = Application.builder().token(YOUR_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # Start the bot
    print("✅ Bot is running! Press Ctrl+C to stop")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
