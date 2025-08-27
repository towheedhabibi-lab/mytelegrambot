import os
import requests
from yt_dlp import YoutubeDL
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# گرفتن توکن از Environment Variable
TOKEN = os.getenv("TELEGRAM_TOKEN")

# وقتی کاربر /start بزند
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 🎵 اسم آهنگ رو بفرست تا برات لینک دانلود بیارم!")

# وقتی کاربر اسم آهنگ بفرستد
async def search_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text("⏳ در حال جستجو هستم...")

    try:
        # جستجو در یوتیوب
        ydl_opts = {"format": "bestaudio", "noplaylist": True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]
            url = info["url"]
            title = info["title"]

        await update.message.reply_text(f"🎶 {title}\n\n🔗 {url}")

    except Exception as e:
        await update.message.reply_text("❌ خطا در گرفتن لینک! دوباره تلاش کن.")
        print("Error:", e)

# اجرای ربات
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_song))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
