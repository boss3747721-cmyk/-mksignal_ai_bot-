import asyncio
import random
import logging
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from datetime import datetime, timezone
from telegram import Update
from telegram.ext import ApplicationBuilder, Application, CommandHandler, ContextTypes

# ==================== কনফিগারেশন ====================
TOKEN = "8665132024:AAFqHP1LTJ3HwLOrpm_8sDVk_QtjBYmLGAM"  # আপনার নতুন BotFather Token
CHAT_ID = -1003927709512  # আপনার নতুন চ্যানেলের Chat ID (Integer হিসেবে)

# আপনার দেওয়া Win (Dance) এবং Loss (Crying) স্টিকারের File ID
STICKER_WIN_DANCE = "CAACAgUAAxkBAAERot1qbC72HGPW4eOdWUX2Q1Oyl_hXNgACqRkAAo1duFRYOEDNU42Lqj0E"
STICKER_LOSS_CRY  = "CAACAgUAAxkBAAERot9qbC769-bIeXphPRLx04u58su-JQAC2xYAAgUNwFTuWZdkTTTthz0E"
# ===================================================

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# Render-এর Deploying আটকে যাওয়া বন্ধ করার জন্য Fake Web Server
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Running Perfectly!")

def run_health_check_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# গেমের সময় গণনা করার ফাংশন (UTC টাইম অনুযায়ী)
def get_current_period():
    now = datetime.now(timezone.utc)
    total_seconds = now.hour * 3600 + now.minute * 60 + now.second
    period_num = (total_seconds // 30) + 1
    date_str = now.strftime("%Y%m%d")
    full_period_id = f"{date_str}10005{period_num:04d}"
    
    remaining_seconds = 30 - (now.second % 30)
    return full_period_id, remaining_seconds

# লাইভ অটো সিগনাল ও ফল প্রকাশ লুপ
async def auto_signal_engine(app: Application):
    last_prediction = None
    last_period_id = None

    while True:
        period_id, remaining_time = get_current_period()
        
        if remaining_time > 0:
            await asyncio.sleep(remaining_time)
            period_id, _ = get_current_period()

        if period_id != last_period_id:
            last_period_id = period_id

            # ১. আগের সিগনালের ফলাফল অনুযায়ী স্টিকার পাঠানো
            if last_prediction is not None:
                actual_result = random.choice(["BIG", "SMALL"])
                is_win = (last_prediction == actual_result)
                
                try:
                    if is_win:
                        # Win হলে ডান্স স্টিকার
                        await app.bot.send_sticker(chat_id=CHAT_ID, sticker=STICKER_WIN_DANCE)
                    else:
                        # Loss হলে কান্নার স্টিকার
                        await app.bot.send_sticker(chat_id=CHAT_ID, sticker=STICKER_LOSS_CRY)
                except Exception as e:
                    print(f"Sticker Send Error: {e}")

            # ২. নতুন সিগনাল তৈরি
            chosen_type = random.choice(["BIG", "SMALL"]) 
            last_prediction = chosen_type
            
            if chosen_type == "BIG":
                number = random.randint(5, 9)
                prediction_icon = "BIG 🔼"
            else:
                number = random.randint(0, 4)
                prediction_icon = "SMALL 🔽"

            # আপনার ফরম্যাট অনুযায়ী মেসেজ
            signal_msg = (
                f"🎯 WINGO 30-S LIVE SIGNAL 🎯\n\n"
                f"📡 PERIOD: #{period_id[-4:]}\n"
                f"📊 NUMBER: #{number}\n"
                f"🔮 PREDICTION: {prediction_icon}\n\n"
                f"🤖 MK Trader Ai Prediction"
            )

            try:
                await app.bot.send_message(chat_id=CHAT_ID, text=signal_msg)
            except Exception as e:
                print(f"Signal Send Error: {e}")

        await asyncio.sleep(1)

async def post_init(app: Application):
    asyncio.create_task(auto_signal_engine(app))

if __name__ == '__main__':
    # Web Server-কে ব্যাকগ্রাউন্ডে চালু করা হচ্ছে যাতে Render-এ আটকে না যায়
    Thread(target=run_health_check_server, daemon=True).start()
    
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    print("🤖 MK Trader Ai Live Bot Started...")
    app.run_polling()                try:
                    if is_win:
                        # Win হলে ডান্স স্টিকার
                        await app.bot.send_sticker(chat_id=CHAT_ID, sticker=STICKER_WIN_DANCE)
                    else:
                        # Loss হলে কান্নার স্টিকার
                        await app.bot.send_sticker(chat_id=CHAT_ID, sticker=STICKER_LOSS_CRY)
                except Exception as e:
                    print(f"Sticker Send Error: {e}")

            # ২. নতুন সিগনাল তৈরি
            chosen_type = random.choice(["BIG", "SMALL"]) 
            last_prediction = chosen_type
            
            if chosen_type == "BIG":
                number = random.randint(5, 9)
                prediction_icon = "BIG 🔼"
            else:
                number = random.randint(0, 4)
                prediction_icon = "SMALL 🔽"

            # আপনার ফরম্যাট অনুযায়ী মেসেজ
            signal_msg = (
                f"🎯 WINGO 30-S LIVE SIGNAL 🎯\n\n"
                f"📡 PERIOD: #{period_id[-4:]}\n"
                f"📊 NUMBER: #{number}\n"
                f"🔮 PREDICTION: {prediction_icon}\n\n"
                f"🤖 MK Trader Ai Prediction"
            )

            try:
                await app.bot.send_message(chat_id=CHAT_ID, text=signal_msg)
            except Exception as e:
                print(f"Signal Send Error: {e}")

        await asyncio.sleep(1)

async def post_init(app: Application):
    asyncio.create_task(auto_signal_engine(app))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    print("🤖 MK Trader Ai Live Bot Started...")
    app.run_polling()        
        if remaining_time > 0:
            await asyncio.sleep(remaining_time)
            period_id, _ = get_current_period()

        if period_id != last_period_id:
            last_period_id = period_id

            # ১. আগের সিগনালের ফলাফল অনুযায়ী স্টিকার পাঠানো
            if last_prediction is not None:
                actual_result = random.choice(["BIG", "SMALL"])
                is_win = (last_prediction == actual_result)
                
                try:
                    if is_win:
                        # Win হলে ডান্স স্টিকার
                        await app.bot.send_sticker(chat_id=CHAT_ID, sticker=STICKER_WIN_DANCE)
                    else:
                        # Loss হলে কান্নার স্টিকার
                        await app.bot.send_sticker(chat_id=CHAT_ID, sticker=STICKER_LOSS_CRY)
                except Exception as e:
                    print(f"Sticker Send Error: {e}")

            # ২. নতুন সিগনাল তৈরি
            chosen_type = random.choice(["BIG", "SMALL"]) 
            last_prediction = chosen_type
            
            if chosen_type == "BIG":
                number = random.randint(5, 9)
                prediction_icon = "BIG 🔼"
            else:
                number = random.randint(0, 4)
                prediction_icon = "SMALL 🔽"

            # আপনার ফরম্যাট অনুযায়ী মেসেজ
            signal_msg = (
                f"🎯 WINGO 30-S LIVE SIGNAL 🎯\n\n"
                f"📡 PERIOD: #{period_id[-4:]}\n"
                f"📊 NUMBER: #{number}\n"
                f"🔮 PREDICTION: {prediction_icon}\n\n"
                f"🤖 MK Trader Ai Prediction"
            )

            try:
                await app.bot.send_message(chat_id=CHAT_ID, text=signal_msg)
            except Exception as e:
                print(f"Signal Send Error: {e}")

        await asyncio.sleep(1)

async def post_init(app: Application):
    asyncio.create_task(auto_signal_engine(app))

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    print("🤖 MK Trader Ai Live Bot Started...")
    app.run_polling()
