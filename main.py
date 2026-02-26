import os
import telebot
from flask import Flask, request

# ===== TOKEN =====
TOKEN = os.environ["TOKEN"]

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ===== COMMANDS =====
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot is working 🚀")

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, message.text)

# ===== WEBHOOK =====
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "Bot is running!"

# ===== RUN =====
if __name__ == "__main__":
    bot.remove_webhook()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
