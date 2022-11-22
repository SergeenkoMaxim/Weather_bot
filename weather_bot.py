import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
from url_for_weather import urls_for_current_forecast

user_city = ' '
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81'
}

bot = telebot.TeleBot('5746705351:AAEjburxVyO6EJN6F_RxrN0hefcOBqOEUhc')
bot.set_webhook()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}, для выбора города напиши /city")


@bot.message_handler(commands=['city'])
def show_keyboard(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    button_brest = types.KeyboardButton("Брест")
    button_vitebsk = types.KeyboardButton("Витебск")
    button_gomel = types.KeyboardButton("Гомель")
    button_grodno = types.KeyboardButton("Гродно")
    button_mogilev = types.KeyboardButton("Могилев")
    button_minsk = types.KeyboardButton("Минск")

    markup.add(button_brest, button_vitebsk, button_gomel, button_grodno, button_mogilev, button_minsk)

    bot.send_message(message.chat.id, f"Выбери город", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def print_info(message):
    user_city = message.text.lower()

    url_for_city = urls_for_current_forecast.get(f"{user_city}")

    if url_for_city is None:
        bot.send_message(message.chat.id, f"Город не найден, попробуй снова")

    else:

        page_for_current_forecast = requests.get(url_for_city, headers=headers)
        soup_for_current_forecast = BeautifulSoup(page_for_current_forecast.text, 'lxml')

        current_time = soup_for_current_forecast.find_all('div', class_='day')
        current_weather = soup_for_current_forecast.find_all('div', class_='weather-value')

        for weather in current_weather:
            for time in current_time[0]:
                if weather.text[2] == ' ':
                    bot.send_message(message.from_user.id, f"Погода в городе {user_city[0].upper() + user_city[1::]}"
                                                           f" на {time.text} - {weather.text[0:2]}")

            else:
                for time in current_time[0]:
                    weather.text[0:4].replace(',', '.')
                    bot.send_message(message.from_user.id, f"Погода в городе {user_city[0].upper() + user_city[1::]}"
                                                           f" на {time.text} - {weather.text[0:4]}")


bot.polling(interval=0, timeout=0)
