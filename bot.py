import telebot
import config

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

markup = types.InlineKeyboardMarkup(row_width=2)
PlLanguageButton = types.InlineKeyboardButton("Polski 🇵🇱", callback_data="lang_pl")
RusLanguageButton = types.InlineKeyboardButton("Русский 🇷🇺", callback_data="lang_rus")
portfolioButton = types.InlineKeyboardButton("", callback_data="portfolio")
priceButton = types.InlineKeyboardButton("", callback_data="price")
signButton = types.InlineKeyboardButton("", callback_data="sign")
markup.add(PlLanguageButton, RusLanguageButton)

language = ''

sign = False

@bot.message_handler(commands = ['start'])
def setLanguage(message):
    bot.send_message(message.chat.id, "Привет! Для начала выбери язык\n\n Cześć! Najpierw wybierz język", parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types = ['text'])
def writeData(message):
        global sign
        if sign:
            fileForOrders = open('orders.txt', "a")
            fileForOrders.write(message.text + '\n')
            fileForOrders.close()
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
            if call.data == 'lang_rus':
                language = 'RUS'
                showWelcome(call, language, markup)
            if call.data == 'lang_pl':
                language = 'PL'
                showWelcome(call, language, markup)
            if call.data == 'portfolio':
                showPortfolio(call, language, markup)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="",
                    reply_markup=None)
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
    if language == 'RUS':
        portfolioButton = types.InlineKeyboardButton("Портфолио", callback_data="portfolio")
        priceButton = types.InlineKeyboardButton("Прайс лист", callback_data="price")
        signButton = types.InlineKeyboardButton("Записаться", callback_data="sign")
        markup.add(portfolioButton, priceButton, signButton)
        bot.send_message(call.message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>\nТут ты можешь посмотреть портфолио, цены, а также записаться на ремонт своего ноутбука!".format(call.message.from_user, bot.get_me()),
            parse_mode='html', reply_markup=markup)
    if language == 'PL':
        portfolioButton = types.InlineKeyboardButton("Portfolio", callback_data="portfolio")
        priceButton = types.InlineKeyboardButton("Ceny", callback_data="price")
        signButton = types.InlineKeyboardButton("Zapisać się", callback_data="sign")
        markup.add(portfolioButton, priceButton, signButton)
        bot.send_message(call.message.chat.id, "Witam, {0.first_name}!\nЯ - <b>{1.first_name}</b>\nTutaj możesz obejrzeć portfolio, ceny oraz się zapisać na naprawę swego laptopa!".format(call.message.from_user, bot.get_me()),
            parse_mode='html', reply_markup=markup)


def showPrice(call, language, markup):
    markup = types.InlineKeyboardMarkup(row_width=2)
    global portfolioButton
    global signButton
    if language == 'PL':
        portfolioButton = types.InlineKeyboardButton("Portfolio", callback_data="portfolio")
        signButton = types.InlineKeyboardButton("Zapisać się", callback_data="sign")
        pricelist = open('pricelistPL.txt', "r", encoding='utf-8')
    if language == 'RUS':
        portfolioButton = types.InlineKeyboardButton("Портфолио", callback_data="portfolio")
        signButton = types.InlineKeyboardButton("Записаться", callback_data="sign")
        pricelist = open('pricelistRUS.txt', "r", encoding='utf-8')
    stringForOutput = ''
    for line in pricelist:
        stringForOutput += line + '\n'
    markup.add(portfolioButton, signButton)
    bot.send_message(call.message.chat.id, stringForOutput, parse_mode='html', reply_markup=markup)

def showPortfolio(call, language,  markup):
    global priceButton
    global signButton
    markup = types.InlineKeyboardMarkup(row_width=2)
    if language == 'PL':
        priceButton = types.InlineKeyboardButton("Ceny", callback_data="price")
        signButton = types.InlineKeyboardButton("Zapisać się", callback_data="sign")
        portfolioFile = open('portfolioPL.txt')
    if language == 'RUS':
        priceButton = types.InlineKeyboardButton("Прайс лист", callback_data="price")
        signButton = types.InlineKeyboardButton("Записаться", callback_data="sign")
        portfolioFile = open('portfolioRUS.txt')
    stringForOutput = ''
    for line in portfolioFile:
        stringForOutput += line + '\n'
    markup.add(priceButton, signButton)
    bot.send_message(call.message.chat.id, stringForOutput, parse_mode='html', reply_markup=markup)

bot.polling(none_stop=True)
