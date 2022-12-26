import requests as rq
import xmltodict
import telebot

bot = telebot.TeleBot('TOKEN')


def currency(curr):
    s = rq.get('http://www.cbr.ru/scripts/XML_daily.asp')

    dct = xmltodict.parse(s.text)['ValCurs']['Valute']
    rate = 0.0
    for val in dct:
        if val['CharCode'] == curr:
            rate = float(val["Value"].replace(',', '.')) / int(val["Nominal"])

            return f'Курс валюты {curr} на текущий день ЦБ РФ: \n{val["Name"]} - {rate} руб.'
    else:
        return f'Такой валюты не существует! По пробуй еще раз'


@bot.message_handler(commands=['currency'])
def start_messages(message):
    bot.send_message(message.from_user.id,
                     'Привет могу показать тебе актуальный курс любой валюты.\
                        \nКакая валюта тебя интересует? USD, EUR, CNY, GBP и т.д.')


@bot.message_handler(func=lambda message: message.text)
def currency_messages(message):
    msg = message.text.upper()
    bot.send_message(message.from_user.id, currency(msg))


bot.infinity_polling()
