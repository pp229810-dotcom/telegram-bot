import os
import telebot

TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def reply(message):
    text = message.text.lower()

    if "hi" in text:
        bot.reply_to(message, "Hello 👋")

    elif "price" in text:
        bot.reply_to(message, "Price is 5000 kyats 💰")

    elif "contact" in text:
        bot.reply_to(message, "Contact me 👉 @yourusername")

    else:
        bot.reply_to(message, "I don't understand 🤔")

print("Bot is running...")
bot.infinity_polling()
