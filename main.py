from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from fpl_extract import FplDeadline
from telegram import Bot
import config
import datetime
import os
import signal

with open('pid.txt') as pid_file:
   pid = pid_file.read()

if os.stat('pid.txt').st_size > 0:
    try:
        os.kill(int(pid), signal.SIGINT)
    except:
        pid = None
else:
    pass

os.environ['TZ'] = 'Singapore'

new_pid = os.getpid()
with open ('pid.txt', 'w') as pid_file:
    pid_file.write(str(new_pid))


alert = FplDeadline()
api_token = config.bot_token
bot_chatID = config.bot_chatID
updater = Updater(api_token, use_context=True)
atxfplbot = Bot(token=api_token)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to ATX FPL Deadline Bot! Type '/help' to see available commands.")


def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        """
        Available commands:
        /facebook - Our Facebook page.
        /deadline - Deadline for the next Gameweek.
        /league - Join our private league.
        /price - Price Changes for players
        """
    )


def fb_link(update: Update, context: CallbackContext):
    update.message.reply_text('https://facebook.com/ATXTechExpert')


def deadline(update: Update, context: CallbackContext):
    update.message.reply_text(alert.deadline())


def price_alert(update: Update, context: CallbackContext):
    update.message.reply_text(alert.price())


def league(update: Update, context: CallbackContext):
    update.message.reply_text('https://fantasy.premierleague.com/leagues/auto-join/2v5h4k')


def sendNotification(message):
    atxfplbot.send_message(chat_id=bot_chatID, text=message)


alert.deadline()
# if alert.localtime[alert.countdown].date().isoformat() == datetime.date.today().isoformat():
#     print('True')
# else:
#     print('False')

if alert.localtime[alert.countdown].date().isoformat() == datetime.date.today().isoformat():
    message = f"Gameweek {alert.countdown + 1} \n Deadline date: {alert.localtime[alert.countdown].strftime('%d-%m-%y')} \n Deadline time: {alert.localtime[alert.countdown].strftime('%H:%M:%S')} "
    atxfplbot.send_message(chat_id=bot_chatID, text=message)

updater.dispatcher.add_handler(CommandHandler('start', start))
# updater.dispatcher.add_handler(CommandHandler('noti', sendNotification(message=message)))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('facebook', fb_link))
updater.dispatcher.add_handler(CommandHandler('price', price_alert))
updater.dispatcher.add_handler(CommandHandler('deadline', deadline))
updater.dispatcher.add_handler(CommandHandler('league', league))
updater.start_polling()

