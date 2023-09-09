from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
from responses import show_current_schedule, schedule_generator
from decouple import config
from keep_alive import keep_alive

TOKEN: Final = config("TOKEN", cast=str)
BOT_USERNAME: Final = "@SceleMtiScrapingBot"

keep_alive()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # await update.message.reply_text('Viva viva viva fasilkom! teknik bukan apalagi mipa! This bot will text you if new update on class schedule is posted on scele.')
    # update.message.reply_text(auto_update())
    await update.message.reply_text('Bot started test')

async def show_schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(show_current_schedule())

async def callback_show_message(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context.job.chat_id, text=schedule_generator())
        # context.bot.send_message(chat_id="@SceleMtiScrapingBot",
        #                      text=schedule_generator())

async def auto_show_schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jobs = context.job_queue.jobs()
    chat_id = update.message.chat_id
    name = update.effective_chat.full_name

    if len(jobs) > 0:
        await context.bot.send_message(chat_id=chat_id, text="auto_show is currently running")
    else:
        await context.bot.send_message(chat_id=chat_id, text="Wait for new schedule update.\n The bot will refresh every 30 minutes to check new schedule update.")
        context.job_queue.run_repeating(callback_show_message, interval=1800, first=1, data=name, chat_id=chat_id)

async def stop_sending_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jobs = context.job_queue.jobs()
    chat_id = update.message.chat_id

    if len(jobs) == 0:
        await context.bot.send_message(chat_id=chat_id, text="auto_show not running")
    else:
        # await context.bot.send_message(chat_id=chat_id, text="Stop sending schedule. Are you graduated? On behalf of me as a person who goes through the same trenches, I just wanna say I'm proud! Congraduation!")
        await context.bot.send_message(chat_id=chat_id, text="bot stopped")
        jobs[0].enabled = False
        jobs[0].schedule_removal()
        # print([job.name for job in jobs])

async def reply_unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Dont text me, just command me.')

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('show_schedule', show_schedule_command))
    app.add_handler(CommandHandler('auto_show', auto_show_schedule_command))
    app.add_handler(CommandHandler('stop', stop_sending_schedule))

    app.add_handler(MessageHandler(filters.TEXT, reply_unknown_message))

    app.add_error_handler(error)

    app.run_polling(poll_interval=3)