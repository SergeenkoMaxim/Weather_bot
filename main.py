import requests
from bs4 import BeautifulSoup

url = 'https://www.lamoda.by/c/4153/default-women/?display_locations=regular&multigender_page=0&q=%D1%82%D1%83%D1%84%D0%BB%D0%B8+%D0%B6%D0%B5%D0%BD%D1%81%D0%BA%D0%B8%D0%B5+%D0%BD%D0%B0+%D0%BA%D0%B0%D0%B1%D0%BB%D1%83%D0%BA%D0%B5&submit=y'
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')
item = soup.find_all('div', class_='product-x-product-card-description__product-name-name')
price = soup.find_all('div', class_='x-product-card-description__microdata-wrap')
material = soup.find_all('span', class_='_attributeValue_1lugn_11 ui-product-description-attribute-upper_material')

for i in price:
    print(i.text)

print(item)

# url = 'https://scrapingclub.com/exercise/list_basic/?page=1'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'lxml')
# names = soup.find_all('h4', class_='card-title')
# prices = soup.find_all('h5')

# for i in range(0, len(names)):
#     print(f"{names[i].text} - {prices[i].text}", end='', sep='')

