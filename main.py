#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from db import mongo_engine
from db import json_engine as je

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters , ConversationHandler

GENDER, NAME, LOCATION, BIO = range(4)

users_cache = {}

def testf():
    tj = je.newSimpleJS(name='Johanna', username='@User',city='Moscow', bio='hello world!')
    db = mongo_engine.mongo()
    db.find_by_username('@User')


def echo(bot, update):
    # global count_
    # update.message.reply_text(str(count_))
    # count_ += 1
    # update.message.reply_text(update.message.text)
    print (update.message.chat_id)
    chatid = update.message.chat_id
    bot.sendMessage(chatid, text='test')


def addme(bot, update):
    username = update.message.from_user['username']
    userinfo = {}
    userinfo['username'] = username
    users_cache[username] = userinfo
    update.message.reply_text('Привет! Как тебя зовут?(Для отмены регистрации введи /cancel , а для того, что бы начать '
                              'всё заного - /startover)')
    # name = update.message.text
    # print(name)
    return NAME


def get_name(bot, update):
    reply_keyboard = [['Male', 'Female', 'Other']]
    name = str(update.message.text).strip().replace('{', '').replace('}', '').replace(']', '').replace('[', '') # rewrite as regex[

    print(name)
    uname = update.message.from_user['username'] # refactor as a function?
    userinfo = users_cache[uname]
    userinfo['name'] = name


    update.message.reply_text('Приятно познакомится, %s. \n К какому гендеру ты себя относишь?' % name,
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return GENDER


def get_gender(bot, update):
    gender = update.message.text.strip().replace('{', '').replace('}', '').replace(']', '').replace('[', '')
    uname = update.message.from_user['username']

    userinfo = users_cache[uname]
    userinfo['gender'] = gender
    print(gender)

    update.message.reply_text('В каком городе ты проживаешь? (Можно указать несколько городов)')
    return LOCATION



def get_location(bot,update):
    city = update.message.text.strip().replace('{', '').replace('}', '').replace(']', '').replace('[', '')
    city = str(city).lower()
    print (update.message.from_user)
    uname = update.message.from_user['username']
    userinfo = users_cache[uname]
    userinfo['city'] = city

    print(city)
    update.message.reply_text('Расскажи мне о себе.')
    return BIO


def get_bio(bot, update):
    bio = update.message.text.strip().replace('{', '').replace('}', '').replace(']', '').replace('[', '')

    print(bio)
    uname = update.message.from_user['username']
    userinfo = users_cache[uname]
    userinfo['bio'] = bio

    # print(users_cache[uname])
    # if mongo_engine.mongo.entry_exists(uname):

    mongo_engine.mongo().add_entry(users_cache[uname])
    update.message.reply_text('Ураа! У тебя всё получилось,%s :3' % userinfo['name'])
    del users_cache[uname]
    return ConversationHandler.END


def startover_addme(bot, update):
    username = update.message.from_user['username']
    userinfo = {}
    userinfo['username'] = username
    users_cache[username] = userinfo
    update.message.reply_text('Привет! Как тебя зовут?')
    return NAME


def cancel_addme(bot, update):
    return ConversationHandler.END


def whois(bot, update):
    findname = str(update.message.text)
    findname = findname.replace('@', '').replace('/whois', '').strip()
    db = mongo_engine.mongo()
    result = db.find_by_username(username=findname)
    if result:
        response = list()
        # response.append('')
        response.append(result['name'] + '\n')
        response.append(result['city'] + '\n')
        response.append(result['bio'])
        update.message.reply_text(''.join(response))
    else:
        update.message.reply_text('not found')


def main():
    with open('/home/gss/python/polytg-bot/token')as f:
        token = str(f.read())

    token = token.strip()
    updater = Updater(token)
    dp = updater.dispatcher
    # dp.add_handler(CommandHandler("addme", addme))
    # dp.add_handler(MessageHandler(Filters.text, echo))

    addme_handler = ConversationHandler(
        entry_points=[CommandHandler('addme', addme)],

        states={
            NAME: [MessageHandler(Filters.text, get_name),
                   CommandHandler('cancel', cancel_addme),
                   CommandHandler('startover', startover_addme)],

            GENDER: [MessageHandler(Filters.text, get_gender),
                     CommandHandler('cancel', cancel_addme),
                     CommandHandler('startover', startover_addme)],

            LOCATION: [MessageHandler(Filters.text, get_location),
                     CommandHandler('cancel', cancel_addme),
                     CommandHandler('startover', startover_addme)],

            BIO: [MessageHandler(Filters.text, get_bio),
                     CommandHandler('cancel', cancel_addme),
                     CommandHandler('startover', startover_addme)],
        },
        fallbacks=[CommandHandler('cancel', cancel_addme)]
    )

    dp.add_handler(addme_handler)
    dp.add_handler(CommandHandler('echo', echo))
    dp.add_handler(CommandHandler('whois', whois))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
