import telebot
import config

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

markup = types.InlineKeyboardMarkup(row_width=3)
portfolioButton = types.InlineKeyboardButton("Портфолио", callback_data="portfolio")
priceButton = types.InlineKeyboardButton("Прайс лист", callback_data="price")
signButton = types.InlineKeyboardButton("Записаться", callback_data="sign")
markup.add(portfolioButton, priceButton, signButton)

sign = False

@bot.message_handler(commands = ['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>\nТут ты можешь посмотреть портфолио, цены, а также записаться на ремонт своего ноутбука!".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types = ['text'])
def writeData(message):
        global sign
        if sign:
            fileForOrders = open('orders.txt', "a")
            fileForOrders.write(message.text + '\n')
            fileForOrders.close()
            sign = False
            bot.send_message(message.chat.id, "Заказ принят, скоро с вами свяжуться!")
            welcome(message)
        else:
            bot.send_message(message.chat.id, "Выбери кнопку")

@bot.callback_query_handler(func=lambda call: True)
def welcome_callback(call):
    global sign
    try:
        if call.message:
            if call.data == 'portfolio':
                showPortfolio(call)
            elif call.data == 'price':
                showPrice(call)
            elif call.data == "sign":
                sign = True
                bot.send_message(call.message.chat.id, "Впиши модель ноутбука, свое имя и номер телефона через пробел, пример:\n HP dolboeb Artur +482281337\n Проверь чтоб все было правильно!",
                    parse_mode='html')
    except Exception as e:
        print(repr(e))

def showPrice(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(portfolioButton, signButton)
    pricelist = open('pricelist.txt', "r", encoding='utf-8')
    stringForOutput = ''
    for line in pricelist:
        stringForOutput += line + '\n'
    bot.send_message(call.message.chat.id, stringForOutput, parse_mode='html', reply_markup=markup)

def showPortfolio(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(priceButton, signButton)
    portfolioFile = open('portfolio.txt')
    stringForOutput = ''
    for line in portfolioFile:
        stringForOutput += line + '\n'
    bot.send_message(call.message.chat.id, stringForOutput, parse_mode='html', reply_markup=markup)

bot.polling(none_stop=True)
