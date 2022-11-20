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
    # bot.send_message(message.from_user.id, f"Привет, {message.from_user.first_name}, для корректного использования "
    #                                         f"выберите ваш город")
                                           # f"бота воспользуйся командой /help")

    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}, для выбора города напиши /сity")

    # bot.register_next_step_handler(message, get_city)


@bot.message_handler(commands=['city'])
def show_keyboard(message):
    # markup = types.InlineKeyboardMarkup()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    # button_brest = types.InlineKeyboardButton('Брест', callback_data='brest')
    button_brest = types.KeyboardButton("Брест")
    # button_vitebsk = types.InlineKeyboardButton('Витебск', callback_data='vitebsk')
    # button_gomel = types.InlineKeyboardButton('Гомель', callback_data='gomel')
    # button_grodno = types.InlineKeyboardButton('Гродно', callback_data='grodno')
    # button_mogilev = types.InlineKeyboardButton('Могилев', callback_data='mogilev')
    # button_minsk = types.InlineKeyboardButton('Минск', callback_data='minsk')

    # markup.add(button_brest, button_vitebsk, button_gomel, button_grodno, button_mogilev, button_minsk)
    markup.add(button_brest)
    bot.send_message(message.chat.id, f"Выбери город", reply_markup=markup)


# @bot.callback_query_handler(func=lambda call: True)
# def set_url(call):
#     global url_for_city
#
#     url_for_city = urls_for_current_forecast.get(f"{call.data}")
#     print(f"{url_for_city} - set_url")


@bot.message_handler(content_types=['text'])
def print_info(message):
    user_city = message.text.lower()

    url_for_city = urls_for_current_forecast.get(f"{user_city}")

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


# @bot.message_handler(commands=["help"])
# def commands(message):
#     bot.send_message(message.from_user.id, f"Воспользуйтесь командой /weather для получения прогноза \n"
#                                                f"Воспользуйтесь командой /change для смены города")
#
#
# @bot.message_handler(commands=["change"])
# def get_city(message):
#
#     bot.send_message(message.from_user.id, f"Введите ваш город!")
#     bot.register_next_step_handler(message, set_city)


# @bot.message_handler(content_types=['text'])
# def set_city(message):
#     global user_city
#     global url_for_city
#
#     user_city = message.text.lower()
#     print(user_city)
#
#     url_for_city = urls_for_current_forecast.get(f"{user_city}")
#     print(f"{url_for_city} - set_city")
#
#     if url_for_city is not None:
#         bot.send_message(message.from_user.id, f"Город {user_city} успешно установлен! \n")
#                                                # f"Для получения прогноза воспользуйтесь командой /weather")
#
#         bot.register_next_step_handler(message, create_soup)
#
#     else:
#         bot.send_message(message.from_user.id, f"Такого города нет в Беларуси, попробуй снова")
#
#         bot.register_next_step_handler(message, set_city)


# @bot.message_handler(commands=['weather'])
# def create_soup(message):
#     global current_time, current_weather
#     page_for_current_forecast = requests.get(url_for_city, headers=headers)
#     soup_for_current_forecast = BeautifulSoup(page_for_current_forecast.text, 'lxml')
#
#     current_time = soup_for_current_forecast.find_all('div', class_='day')
#     current_weather = soup_for_current_forecast.find_all('div', class_='weather-value')
#
#     bot.register_next_step_handler(message, print_information)
#
#
# @bot.message_handler()
# def print_information(message):
#     for weather in current_weather:
#         for time in current_time[0]:
#             if weather.text[2] == ' ':
#                 bot.send_message(message.from_user.id, f"Погода в городе {user_city[0].upper() + user_city[1::]}"
#                                                         f" на {time.text} - {weather.text[0:2]}")
#
#             else:
#                 for time in current_time[0]:
#                     weather.text[0:4].replace(',', '.')
#                     bot.send_message(message.from_user.id, f"Погода в городе {user_city[0].upper() + user_city[1::]}"
#                                                             f" на {time.text} - {weather.text[0:4]}")


bot.polling(interval=0, timeout=0)
