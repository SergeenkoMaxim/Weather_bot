import re
import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
from url_for_weather import urls_for_current_forecast, urls_for_weekly_forecast
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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

    bot.send_message(message.chat.id, "Выбери город", reply_markup=markup)
    bot.register_next_step_handler(message, create_soup)


@bot.message_handler(commands=['week'])
def send_screenshot(message):
    url_for_photo = urls_for_weekly_forecast.get(f"{user_city}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(f'{url_for_photo}')
    driver.get_screenshot_as_file("screenshot.png")
    driver.quit()

    im = Image.open("screenshot.png")
    width, height = im.size
    # box = (200, 492, 1520, 990)
    # cut = (475, 1030, 1790, 1430)
    cut = (200, 870, 1525, 1430)
    im1 = im.crop(cut)
    im1.save("new_screenshot.png")

    photo = open("new_screenshot.png", 'rb')
    bot.send_photo(message.chat.id, photo)


@bot.message_handler()
def create_soup(message):
    global user_city
    global current_time
    global current_weather
    global сurrent_wind
    global current_pressure
    global current_humidity
    global current_water
    global real_feel

    user_city = message.text.lower()

    url_for_city = urls_for_current_forecast.get(f"{user_city}")

    if url_for_city is None:
        bot.send_message(message.chat.id, f"Город не найден, попробуй снова")
        bot.register_next_step_handler(message, show_keyboard)

    else:

        page_for_current_forecast = requests.get(url_for_city, headers=headers)
        soup_for_current_forecast = BeautifulSoup(page_for_current_forecast.text, 'lxml')

        current_time = soup_for_current_forecast.find_all('div', class_='day')
        current_weather = soup_for_current_forecast.find_all('div', class_='weather-value')
        сurrent_wind = soup_for_current_forecast('div', class_='unit unit_wind_m_s')
        current_pressure = soup_for_current_forecast('div', class_='unit unit_pressure_mm_hg_atm')
        current_humidity = soup_for_current_forecast('div', class_='now-info-item humidity')
        current_water = soup_for_current_forecast('div', class_='unit unit_temperature_c')
        real_feel = soup_for_current_forecast('span', class_='unit unit_temperature_c')
        sunset = soup_for_current_forecast.find_all('div', class_='now-astro-sunset')
        sunrise = soup_for_current_forecast.find_all('div', class_='now-astro-sunrise')

        for weather in current_weather:
            if weather.text[2] == ' ':
                temperature = weather.text[0:2]
            else:
                for time in current_time[0]:
                    temperature = weather.text[0:4]

        for time in sunrise:
            result_for_sunset = re.findall(r'\d\d\S\d\d', time.text)

        for time in sunset:
            result_for_sunrise = re.findall(r'\d\S\d\d', time.text)

        for t in current_water:
            water = t.text

        for t in real_feel[1]:
            feel = t.text

        for h in current_humidity:
            humidity = h.text[-3:-1]

        for p in current_pressure:
            pressure = p.text[0:3]

        for w in сurrent_wind:
            wind = w.text[0]

        for hour in current_time[0]:
            time = hour.text

        bot.send_message(message.chat.id, f"Погода в городе {user_city[0].upper()+user_city[1::]} на <b>{time}</b>: \n"
                                          f"️температура: <b>{temperature}°</b> \n"                 #🌡
                                          f"влажность: <b>{humidity}%</b> \n"
                                          f"давление: <b>{pressure} мм/рт.ст</b>  \n"             #💨
                                          f"скорость ветра: <b>{wind} м/с</b> \n"
                                          f"температура воды: <b>{water}°</b> \n"
                                          f"ощущается как: <b>{feel}°</b> \n"
                                          f"восход: <b>{result_for_sunrise[0]}</b> \n"            #🌄
                                          f"закат: <b>{result_for_sunset[0]}</b> \n", parse_mode='HTML')    #🌆


# @bot.message_handler(commands=['week'])
# def send_screenshot(message):
#
#     url_for_photo = urls_for_weekly_forecast.get(f"{user_city}")
#
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     driver.get('url_for_photo')
#     driver.get_screenshot_as_file("screenshot.png")
#     driver.quit()
#
#     im = Image.open("screenshot.png")
#     width, height = im.size
#     box = (200, 492, 1520, 990)
#     im1 = im.crop(box)
#     im1.save("new_screenshot.png")
#
#     photo = open("new_screenshot.png", 'rb')
#     bot.send_photo(message.chat.id, photo)


bot.polling(interval=0, timeout=0)
