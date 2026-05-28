import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "TOKEN"

API_URL = "https://api.coingecko.com/api/v3/simple/price"

coins = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "sol": "solana"
}


async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command = update.message.text.replace("/", "")

    if command not in coins:
        await update.message.reply_text("Unknown coin")
        return

    params = {
        "ids": coins[command],
        "vs_currencies": "usd"
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    price = data[coins[command]]["usd"]

    await update.message.reply_text(
        f"{command.upper()} price: ${price}"
    )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("btc", get_price))
app.add_handler(CommandHandler("eth", get_price))
app.add_handler(CommandHandler("sol", get_price))

print("Bot started...")

app.run_polling()
