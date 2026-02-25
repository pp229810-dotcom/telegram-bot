import os
import telebot
from flask import Flask, request

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ပစ္စည်းစာရင်း
PRODUCTS = {
    "ပန်းသီး": {"price": "၅၀၀ ကျပ်", "qr": "https://raw.githubusercontent.com/pp229810-dotcom/telegram-bot/main/sample_qr.jpg"},
    "orange": {"price": "၇၀၀ ကျပ်", "qr": "https://raw.githubusercontent.com/pp229810-dotcom/telegram-bot/main/sample_qr.jpg"}
}

# Group ရော Channel ရော Private Chat ပါ အကုန်ရအောင်လုပ်ထားတာ
@bot.message_handler(func=lambda message: True)
@bot.channel_post_handler(func=lambda message: True)
def handle_all_messages(message):
    # စာသားပါမှ လုပ်ဆောင်မယ်
    if message.text:
        user_text = message.text.lower().strip()
        
        if user_text in PRODUCTS:
            item = PRODUCTS[user_text]
            caption = f"📦 ပစ္စည်း: {user_text}\n💰 ဈေးနှုန်း: {item['price']}\n\nအောက်ပါ QR ဖြင့် ငွေလွှဲနိုင်ပါသည်။"
            bot.send_photo(message.chat.id, item['qr'], caption=caption)
        
        elif user_text in ["hi", "မင်္ဂလာပါ", "hello"]:
            bot.reply_to(message, "မင်္ဂလာပါခင်ဗျာ! ပစ္စည်းအမည် (ဥပမာ- ပန်းသီး) ဟု ရိုက်ပို့နိုင်ပါသည်။")

# --- Webhook Logic ---
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "Bot is running"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=os.environ.get('RENDER_EXTERNAL_URL') + "/" + TOKEN)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))


