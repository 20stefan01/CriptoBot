import telebot
from Config import keys, TOKEN
from extensions import CryptoConvertor, ConvertionException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следущем формате:\nимя валюты\
    в какую валюту перевести\
    количество переводимой валюты\nЕсли число дробное то вводите через .\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")
        if len(values) != 3:
            if len(values) > 3:
                raise ConvertionException('Слишком много параметров')
            elif len(values) < 3:
                raise ConvertionException('Слишком мало параметров')

        base, quote, amount = values
        total = CryptoConvertor.convert(base, quote, amount)

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду:\n{e}')

    else:
        text = f'Цена {amount} {base} в {quote} - {total}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True, interval=0)
