#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from db import mongo_engine
from db import json_engine as je

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters , ConversationHandler

GENDER, NAME, LOCATION, BIO = range(4)
NEXT, USERCITY = range(2)

users_cache = {}
user_search_state = {}

def testf():
    tj = je.newSimpleJS(name='Johanna', username='@User',city='Moscow', bio='hello world!')
    db = mongo_engine.mongo()
    db.find_by_username('@User')

def pretty_data(result):
    if result:
        response = list()
        # response.append('')
        response.append(result['name'] + '\n')
        response.append(result['city'] + '\n')
        response.append('@' + result['username'] + '\n')
        response.append(result['bio'])
        return ''.join(response)
    else:
        return 'not found'

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
                              'всё заново - /startover)')
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
    update.message.reply_text(pretty_data(result))


def find_users(bot, update):
    # reply_keyboard = [['Male', 'Female', 'Other']]
    update.message.reply_text('В каком городе будем искать?')
    return  USERCITY

def get_user_city(bot, update):
    city = update.message.text.strip().replace('{', '').replace('}', '').replace(']', '').replace('[', '').lower()
    username = update.message.from_user['username']
    print(1)
    # reply_keyboard = [['stop', 'next']]
    # update.message.reply_text('get_user_city',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    user_search_state[username] = {}
    user_search_state[username]['city'] = city
    print(2)
    db = mongo_engine.mongo()
    result = db.find_by_city(city)
    print(3)
    print(result.count(), 'count')
    if result.count() > 0:

        print(4)

        fucking_list = list()
        for e in result:
            fucking_list.append(e)

        # print(fucking_list, ' fucking list')
        # cnt = 0
        for elem in fucking_list:
            # cnt += 1
            # print (pretty_data(elem))
            update.message.reply_text(pretty_data(elem))

            print ('out')
        # for
    return ConversationHandler.END
        # userinfo = user_search_state[username]
        # userinfo['cursor'] = result
        # print(result, ' result in city method')
        # print(userinfo)
        # for e in result:
        #    print ('out')
         #   update.message.reply_text('out')
          #  update.message.reply_text(pretty_data(e))
        # return NEXT
    #else:
    #    print(5)
    #   update.message.reply_text('В таком городе никого не нашель!')
    #    del user_search_state[username]
    #    return ConversationHandler.END


def get_next_users(bot, update):
    pass
#    print (5.1)
#    response = str(update.message.text).strip().replace('{', '').replace('}', '').replace(']', '').replace('[', '').lower()
#    username = update.message.from_user['username']
#    print(response + 'response in get_next_users')

#    reply_keyboard = [['stop', 'next']]
#    update.message.reply_text('whattodo',
#                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

#    print(user_search_state, 'user search state')
    # в конец?
#    print(response)
 #   if response == 'next':
 #       print(11)
 #       cursor = user_search_state[username]['cursor']
  #      print(user_search_state[username]['cursor'])
   #     print(11.05)
    #    print('coursor count: ')
     #   print(cursor.count() + ' coursor_count')
      #  print(cursor.alive())

       # print(user_search_state[username]['cursor'])

#        print('before .hasNext')
#        print(cursor.hasNext)
#        if cursor.hasNext():
#            print('11.1')
#            print(cursor.next)
#            #update.message.reply_text(pretty_data(cursor.next()))
#            return NEXT
#        else:
#            print('11.2')
#            update.message.reply_text('Это все. Все остальные уехали в Москву.')
#            del user_search_state[username]
#            return ConversationHandler.END
        # its not a city! :>
        #return result, add cursor to user_search_state
 #   elif response == 'stop':
#        print(12)
 #       del user_search_state[username]
#        # stop conversation
#        return ConversationHandler.END
#    else:
#        update.message.reply_text('Произошла ошибка. Я покажу себе выход.')
#        del user_search_state[username]
#        return ConversationHandler.END
    # print(13)
    # reply_keyboard = [['stop', 'next']]
    # update.message.reply_text('whattodo', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    # return NEXT



def stop_search(bot, update):
    return ConversationHandler.END

def help(bot, update):
    info = 'Интерфейс бота:\n' \
           '/addme - добавить себя в список анкет. Лучше писть в ЛС боту \n' \
           '/whois @username - поиск анкет по юзернейму \n' \
           '/help - это сообщение \n' \
           '/find - поиск анкет по городу. Не чувствительно к регистру. Прка не умею в англ. названия, списки и аббревиатуры.'
    update.message.reply_text(info)

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

    find_handler = ConversationHandler(
        entry_points=[CommandHandler('find', find_users)],

        states={
            NEXT: [MessageHandler(Filters.text, get_next_users)],
            USERCITY: [MessageHandler(Filters.text, get_user_city)]
        },
        fallbacks=[CommandHandler('stop', stop_search)]
    )

    dp.add_handler(find_handler)
    dp.add_handler(addme_handler)
    dp.add_handler(CommandHandler('echo', echo))
    dp.add_handler(CommandHandler('whois', whois))
    dp.add_handler(CommandHandler('help', help))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
