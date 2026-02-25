
import os
import telebot
from flask import Flask, request

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ၁။ စမ်းသပ်ဖို့ ပစ္စည်းစာရင်း (ဒီမှာ လိုသလို ထပ်တိုးနိုင်ပါတယ်)
PRODUCTS = {
    "ပန်းသီး": {"price": "၅၀၀ ကျပ်", "qr": "https://raw.githubusercontent.com/pp229810-dotcom/telegram-bot/main/sample_qr.jpg"},
    "orange": {"price": "၇၀၀ ကျပ်", "qr": "https://raw.githubusercontent.com/pp229810-dotcom/telegram-bot/main/sample_qr.jpg"}
}

# စာသားတွေ စစ်ဆေးတဲ့ Function
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text.lower().strip()
    
    # ပစ္စည်းနာမည်နဲ့ တိုက်စစ်ခြင်း
    if user_text in PRODUCTS:
        item = PRODUCTS[user_text]
        caption = f"📦 ပစ္စည်း: {user_text}\n💰 ဈေးနှုန်း: {item['price']}\n\nအောက်ပါ QR ဖြင့် ငွေလွှဲနိုင်ပါသည်။"
        bot.send_photo(message.chat.id, item['qr'], caption=caption)
    
    # နှုတ်ဆက်စာ
    elif user_text in ["hi", "မင်္ဂလာပါ", "hello"]:
        bot.reply_to(message, "မင်္ဂလာပါခင်ဗျာ! ပစ္စည်းဈေးနှုန်းသိလိုပါက ပစ္စည်းအမည် (ဥပမာ- ပန်းသီး) ဟု ရိုက်ပို့နိုင်ပါသည်။")
    
    # မသိတဲ့စာဆိုရင် ပြန်ပြောမယ့်စာ
    else:
        bot.reply_to(message, f"စိတ်မရှိပါနဲ့၊ '{message.text}' ဆိုတာကို နားမလည်လို့ပါ။ 'hi' လို့ ရိုက်ပို့ကြည့်ပါ။")

# --- Render Webhook Logic (မဖျက်ပါနဲ့) ---
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
