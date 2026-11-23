import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import datetime

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبا! صيفط ليا الموعد هكا:\n/remind 25-11-2026 18:00 موعد في دار الثقافة مع سيف الدين")

async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.split(" ", 3)
        date_str = text[1]
        time_str = text[2]
        msg = text[3]
        dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M")
        delay = (dt - datetime.datetime.now()).total_seconds()
        if delay < 0:
            await update.message.reply_text("هاد الوقت داز، عطيني وقت جاي")
            return
        context.job_queue.run_once(send_reminder, delay, chat_id=update.effective_chat.id, data=msg)
        await update.message.reply_text(f"واخا! غادي نفكرك فـ {date_str} مع {time_str} : {msg}")
    except:
        await update.message.reply_text("الطريقة غالطة، صيفط هكا:\n/remind 25-11-2026 18:00 موعد في دار الثقافة")

async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text=f"⏰ وصل الوقت!\n{context.job.data}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("remind", remind))
app.run_polling()