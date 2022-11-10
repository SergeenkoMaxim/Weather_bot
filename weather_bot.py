import telebot
import requests
from bs4 import BeautifulSoup
from url_for_weather import urls_for_current_forecats


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81'
}

bot = telebot.TeleBot('5746705351:AAEjburxVyO6EJN6F_RxrN0hefcOBqOEUhc')


@bot.message_handler(content_types=['text'], commands=['start'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, f"Привет, {message.from_user.first_name}, из какого ты города?")
        bot.register_next_step_handler(message, get_city)
    else:
        bot.send_message(message.from_user.id, 'Напиши /start')


@bot.message_handler(content_types=['text'])
def get_city(message):  #get city
    # is_exist = True
    user_city = message.text.lower()

    for key, value in urls_for_current_forecats.items():
        if key == user_city:
            # is_exist = True
            url_for_city = value
        # else:
        #     is_exist = False
    # bot.register_next_step_handler(message, create_soup(url_for_city, user_city))

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

    # if is_exist is False:
    #     bot.send_message(message.from_user.id, f"Такого города нет в Беларуси! Попробуй снова:)")


# @bot.message_handler(content_types=['text'], commands=['/weather'])
# def create_soup(message, url_for_city, user_city):
#
#     page_for_current_forecast = requests.get(url_for_city, headers=headers)
#     soup_for_current_forecast = BeautifulSoup(page_for_current_forecast.text, 'lxml')
#     current_time = soup_for_current_forecast.find_all('div', class_='day')
#     current_weather = soup_for_current_forecast.find_all('div', class_='weather-value')
#
#     for weather in current_weather:
#         for time in current_time[0]:
#             if weather.text[2] == ' ':
#                 bot.send_message(message.from_user.id, f"Погода в городе {user_city[0].upper() + user_city[1::]}"
#                                                        f" на {time.text} - {weather.text[0:2]}")
#         else:
#             for time in current_time[0]:
#                 weather.text[0:4].replace(',', '.')
#                 bot.send_message(message.from_user.id, f"Погода в городе {user_city[0].upper() + user_city[1::]}"
#                                                        f" на {time.text} - {weather.text[0:4]}")

    # bot.register_next_step_handler(message, print_weather)


# @bot.message_handler(content_types=['text'], commands=['/weather'])
# def print_weather(message, current_weather, current_time, user_city):
#
#     for weather in current_weather:
#         for time in current_time[0]:
#             if weather.text[2] == ' ':
#                 bot.send_message(message.from_user.id, f"Погода в городе {user_city[0].upper() + user_city[1::]}"
#                                                        f" на {time.text} - {weather.text[0:2]}")
#         else:
#             for time in current_time[0]:
#                 weather.text[0:4].replace(',', '.')
#                 bot.send_message(message.from_user.id, f"Погода в городе {user_city[0].upper() + user_city[1::]}"
#                                                        f" на {time.text} - {weather.text[0:4]}")


bot.polling(none_stop=True, interval=0)
