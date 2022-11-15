import requests
from bs4 import BeautifulSoup
from url_for_weather import urls_for_current_forecast, urls_for_weekly_forecast
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import schedule
import time


def get_policy():
    global policy
    policy = input("Do u want to get a current forecast or weekly forecast? (current/weekly): ")


def get_user_city():
    global user_city
    user_city = input('Enter your city: ').lower()


get_user_city()
get_policy()


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
# page_for_weekly_forecast = requests.get(url_for_weekly_forecast, headers=headers)

soup_for_currrent_forecast = BeautifulSoup(page_for_current_forecast.text, 'lxml')
# soup_for_weekly_forecast = BeautifulSoup(page_for_weekly_forecast.text, 'lxml')

current_time = soup_for_currrent_forecast.find_all('div', class_='day')
current_weather = soup_for_currrent_forecast.find_all('div', class_='weather-value')

# weekly_day_date = soup_for_weekly_forecast.find_all('div', class_='widget-row widget-row-days-date')
# day_temperature = soup_for_weekly_forecast('div', class_='widget-row-chart widget-row-chart-temperature')
# night_temperature = soup_for_weekly_forecast('div', class_='mint')


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


# def print_weekly_day():
#
#     spisok = []
#
#     for day in weekly_day_date:
#         spisok.append(day.text)
#
#     del spisok[1::]
#
#     print(spisok)


# def print_weekly_temperature():
#
#     print('Day:')
#
#     for i in day_temperature:
#         print(i.text, end=' ')


def print_current_forecast():
    print(f"Weather in {print_city()} at {print_time()} - {print_current_temperature()}")


# def print_weekly_forecast():
#     print(print_weekly_day())
#     print(print_weekly_temperature())

# def print_screenshot(url_for_weekly_forecast):
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--start-maximized")
#
#     driver = webdriver.Chrome('./chromedriver', options=chrome_options)
#     driver.get(url_for_weekly_forecast)
#
#     # element = driver.find_element_by_xpath('///widget-items')
#     element = driver.find_element("name", "selection")
#     width = 1920
#     height = element.size['height'] + 1080
#     driver.set_window_size(width, height)
#     time.sleep(2)
#     driver.save_screenshot('screenshot.png')
#     driver.quit()


if policy == '1':
    print_current_forecast()
elif policy == '2':
    pass
    # print_screenshot(url_for_weekly_forecast)
    # print_weekly_forecast()

# schedule.every(5).seconds.do(print_current_forecast)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
