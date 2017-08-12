#!/usr/bin/env python3
from db import mongo_engine
from db import json_engine as je
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

def testf():
    tj = je.newSimpleJS(name='Johanna', username='@User',city='Moscow', bio='hello world!')
    db = mongo_engine.mongo()
    db.find_by_username('@User')


def addme(bot, update):
    update.message.reply_text('Hi!')
    print('got msg!')

def main():
    updater = Updater('TOKEN')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("addme", addme))

    updater.start_polling()
    updater.idle()
    # testf()


if __name__ == "__main__":
    main()
