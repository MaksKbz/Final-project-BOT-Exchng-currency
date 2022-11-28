
import telebot
from extensions import ExchangeException, Exchange
from token_value import keys, TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Я БОТ-конвертер валют, привет!  \n- СМОТРЕТЬ список валют набери команду- /values \
    \n- Как конвертировать ? набирайте - /help \
\n- Начать программу заново - /start'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать конвертацию, введите команду боту в следующем формате через пробел: \
     \n<имя валюты которая нужна Пример- Евро > <в какой валютой будете платить  Пример - Доллар> <количество нужной валюты Пример - 100> \
     \nИтого надо написать: | Евро Доллар 100 | \nЧтобы увидеть список всех доступных валют, введите команду- /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ExchangeException('Жду ввода данных\n Забыли как пользоваться ? набирайте /help ')

        quote, base, amount = values
        total_base = Exchange.get_price(quote, base, amount)
    except ExchangeException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Что-то пошло не так с {e}')
    else:
        text = f'Обмен {base} на {quote}\n{total_base}  = {amount}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop = True)

