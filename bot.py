import telebot
import config
import sqlite3
import dbHandler
from dbHandler import myCursor, connection

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

markup = types.InlineKeyboardMarkup(row_width=2)
PlLanguageButton = types.InlineKeyboardButton("Polski 🇵🇱", callback_data="lang_pl")
RusLanguageButton = types.InlineKeyboardButton("Русский 🇷🇺", callback_data="lang_rus")
portfolioButton = types.InlineKeyboardButton("", callback_data="portfolio")
priceButton = types.InlineKeyboardButton("", callback_data="price")
signButton = types.InlineKeyboardButton("", callback_data="sign")
markup.add(PlLanguageButton, RusLanguageButton)


adminChatId = 0 #admin chat id for sending new orders to him 

language = ''

sign = False

@bot.message_handler(commands = ['start'])
def setLanguage(message):
    global adminChatId
    bot.send_message(message.chat.id, "Привет! Для начала выбери язык\n\n Cześć! Najpierw wybierz język", parse_mode='html', reply_markup=markup)
    

@bot.message_handler(content_types = ['text'])
def writeData(message):
        global sign
        global adminChatId
        if sign:
            dbHandler.write_order(message.text)
            if adminChatId != -1:
                bot.send_message(adminChatId, message.text)
            sign = False
            markup = types.InlineKeyboardMarkup(row_width=1)
            goBackButton = types.InlineKeyboardButton('Ok', callback_data='back_to_welcome')
            markup.add(goBackButton)
            if language == 'RUS':
                bot.send_message(message.chat.id, "Заказ принят, скоро с вами свяжуться!", parse_mode='html', reply_markup=markup)
            elif language == 'PL':
                bot.send_message(message.chat.id, "Gotowe, z tobą się skontaktują jak można najszybciej!", parse_mode='html', reply_markup=markup)
        else:
            if language == 'RUS':
                bot.send_message(message.chat.id, "Выбери кнопку")
            elif language == 'PL':
                bot.send_message(message.chat.id, "Wybierz przycisk")
        

@bot.callback_query_handler(func=lambda call: True)
def welcome_callback(call):
    global portfolioButton
    global priceButton
    global signButton
    global language
    global sign
    markup = types.InlineKeyboardMarkup(row_width=3)
    try:
        if call.message:
            if call.data == 'back_to_welcome':
                showWelcome(call, language, markup)
            elif call.data == 'lang_rus':
                language = 'RUS'
                showWelcome(call, language, markup)
            elif call.data == 'lang_pl':
                language = 'PL'
                showWelcome(call, language, markup)
            elif call.data == 'portfolio':
                showPortfolio(call, language, markup)
            elif call.data == 'price':
                showPrice(call, language, markup)
            elif call.data == "sign":
                sign = True
                if language == 'PL':
                    bot.send_message(call.message.chat.id, "Wpisz swój model laptopa, imię oraz numer telefonu przez spację, na przykład:\n HP dolboeb Artur +482281337\n sprawdź, by wszystko było poprawne!",
                        parse_mode='html')
                if language == 'RUS':
                    bot.send_message(call.message.chat.id, "Впиши модель ноутбука, свое имя и номер телефона через пробел, пример:\n HP dolboeb Artur +482281337\n Проверь чтоб все было правильно!",
                        parse_mode='html')
    except Exception as e:
        print(repr(e))

def showWelcome(call, language, markup):
    firstName = call.message.chat.first_name
    if language == 'RUS':
        portfolioButton = types.InlineKeyboardButton("Портфолио", callback_data="portfolio")
        priceButton = types.InlineKeyboardButton("Прайс лист", callback_data="price")
        signButton = types.InlineKeyboardButton("Записаться", callback_data="sign")
        markup.add(portfolioButton, priceButton, signButton)
        bot.send_message(call.message.chat.id, "Добро пожаловать, <b>"+firstName+"</b>!\nЯ - <b>{1.first_name}</b>\nТут ты можешь посмотреть портфолио, цены, а также записаться на ремонт своего ноутбука!".format(call.message.from_user, bot.get_me()),
            parse_mode='html', reply_markup=markup)
    if language == 'PL':
        portfolioButton = types.InlineKeyboardButton("Portfolio", callback_data="portfolio")
        priceButton = types.InlineKeyboardButton("Ceny", callback_data="price")
        signButton = types.InlineKeyboardButton("Zapisać się", callback_data="sign")
        markup.add(portfolioButton, priceButton, signButton)
        bot.send_message(call.message.chat.id, "Witam, <b>"+firstName+"</b>!\nJa - <b>{1.first_name}</b>\nTutaj możesz obejrzeć portfolio, ceny oraz się zapisać na naprawę swego laptopa!".format(call.message.from_user, bot.get_me()),
            parse_mode='html', reply_markup=markup)


def showPrice(call, language, markup):
    markup = types.InlineKeyboardMarkup(row_width=2)
    global portfolioButton
    global signButton
    stringForOutput = ''
    if language == 'PL':
        portfolioButton = types.InlineKeyboardButton("Portfolio", callback_data="portfolio")
        signButton = types.InlineKeyboardButton("Zapisać się", callback_data="sign")
        stringForOutput = dbHandler.get_pricesPL()
    if language == 'RUS':
        portfolioButton = types.InlineKeyboardButton("Портфолио", callback_data="portfolio")
        signButton = types.InlineKeyboardButton("Записаться", callback_data="sign")
        stringForOutput = dbHandler.get_pricesRU()
    markup.add(portfolioButton, signButton)
    bot.send_message(call.message.chat.id, stringForOutput, parse_mode='html', reply_markup=markup)

def showPortfolio(call, language,  markup):
    global priceButton
    global signButton
    markup = types.InlineKeyboardMarkup(row_width=2)
    if language == 'PL':
        priceButton = types.InlineKeyboardButton("Ceny", callback_data="price")
        signButton = types.InlineKeyboardButton("Zapisać się", callback_data="sign")
    if language == 'RUS':
        priceButton = types.InlineKeyboardButton("Прайс лист", callback_data="price")
        signButton = types.InlineKeyboardButton("Записаться", callback_data="sign")
    #TO DO 

bot.polling(none_stop=True)
