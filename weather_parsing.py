import os
import requests
from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from PIL import Image

from url_for_weather import urls_for_current_forecast, urls_for_weekly_forecast
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import schedule
import time


# def get_policy():
#     global policy
#     policy = input("Do u want to get a current forecast or weekly forecast? (current/weekly): ")


def get_user_city():
    global user_city
    # user_city = input('Enter your city: ').lower()
    user_city = 'minsk'


get_user_city()
# get_policy()


def get_url():
    global url_for_current_forecast

    for key, value in urls_for_current_forecast.items():
        if key == user_city:
            url_for_current_forecast = value
            return True



# for key, value in urls_for_weekly_forecast.items():
#     if key == user_city:
#         url_for_weekly_forecast = value

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.'
                  '36 OPR/40.0.2308.81'
}
if get_url():
    get_url()
else:
    print("Error")

page_for_current_forecast = requests.get(url_for_current_forecast, headers=headers)

soup_for_currrent_forecast = BeautifulSoup(page_for_current_forecast.text, 'lxml')

current_time = soup_for_currrent_forecast.find_all('div', class_='day')
current_weather = soup_for_currrent_forecast.find_all('div', class_='weather-value')
сurrent_wind = soup_for_currrent_forecast('div', class_='unit unit_wind_m_s')
current_pressure = soup_for_currrent_forecast('div', class_='unit unit_pressure_mm_hg_atm')
current_humidity = soup_for_currrent_forecast('div', class_='now-info-item humidity')
current_water = soup_for_currrent_forecast('div', class_='unit unit_temperature_c')
real_feel = soup_for_currrent_forecast('div', class_='unit unit_temperature_c')


def print_water_temperature():
    for t in current_water:
        return t.text


def print_real_feel():
    for t in real_feel:
        return t.text


def print_humidity():
    for h in current_humidity:
        return h.text[-3:-1]


def print_pressure():
    for p in current_pressure:
        return p.text[0:3]


def print_wind():
    for w in сurrent_wind:
        return f"{w.text[0]} м/с"

def print_time():
    for hour in current_time[0]:
        return hour.text


def print_city():
    city_to_print = user_city[0].upper() + user_city[1::]
    return city_to_print


def print_current_temperature():
    for weather in current_weather:
        if weather.text[2] == ' ':
            return weather.text[0:2]
        else:
            return weather.text[0:4].replace(',', '.')


def print_current_forecast():
    print(f"Weather in {print_city()} at {print_time()}: \n"
          f"температура - {print_current_temperature()}° \n"
          f"скорость ветра - {print_wind()} \n"
          f"давление - {print_pressure()} мм/рт.ст \n"
          f"влажность - {print_humidity()}% \n"
          f"температура воды - {print_water_temperature()}° \n" 
          f"ощущается как - {print_real_feel()}°")


def cut_screenshot():
    # url_for_photo = urls_for_weekly_forecast.get(f"mogilev")

    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    # driver.get(f'{url_for_photo}')
    # driver.get_screenshot_as_file("screenshot.png")
    # driver.quit()

    im = Image.open("screenshot.png")
    width, height = im.size
    # box = (200, 492, 1520, 990)
    cut = (200, 870, 1525, 1430)
    im1 = im.crop(cut)
    im1.save("new_screenshot.png")
    im1.show()

    photo = open("new_screenshot.png", 'rb')




cut_screenshot()

    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--start-maximized")
    #
    # driver = webdriver.Chrome('./chromedriver', options=chrome_options)
    # driver.get(url_for_weekly_forecast)
    #
    # # element = driver.find_element_by_xpath('///widget-items')
    # element = driver.find_element("name", "selection")
    # width = 1920
    # height = element.size['height'] + 1080
    # driver.set_window_size(width, height)
    # time.sleep(2)
    # driver.save_screenshot('screenshot.png')
    # driver.quit()


# if policy == '1':
#     print_current_forecast()
# elif policy == '2':
#     pass


# schedule.every(5).seconds.do(print_current_forecast)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
