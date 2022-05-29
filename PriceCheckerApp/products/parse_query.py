import requests
import lxml
import re
from bs4 import BeautifulSoup

"""
Make a GET request to fetch the raw HTML content
By default, requests sends this header 'User-Agent': 'python-requests/2.22.0,
and this leads to a 404 response being sent to us.
Therefore, we need to inform the server that the
request is coming from the browser
"""

r = requests.get('https://www.perekrestok.ru/',
headers={"User-Agent": "Requests"})
access_token = re.search(r'accessToken":"([^"]+)', r.text).group(1)

class Product:
    def __init__(self, title=None, price=None, picture_url=None):
        self.__title = title
        self.__price = str(price / 100)
        self.__picture_url = picture_url.replace('%s', '400x400-fit')

    @property
    def title(self):
        return self.__title

    @property
    def price(self):
        return self.__price

    @property
    def picture_url(self):
        return self.__picture_url


class Shop:
    def __init__(self, title=None, price=None):
        self.__title = title
        if type(price) == int:
            self.__price = str(price/100) + '0' * \
                (2 - len(str(price/100).split('.')[1]))
        else:
            self.__price = price + '.00'

    @property
    def title(self):
        return self.__title

    @property
    def price(self):
        return self.__price


def parse_request(query):
    url = f'https://www.perekrestok.ru/api/customer/1.4.1.0/catalog/search/all?textQuery={query}&entityTypes[]=product&entityTypes[]=category'
    response = requests.get(
        url, headers={'Authorization': f'Bearer {access_token}'})
    obj_list = []
    for p in response.json()['content']['products']:
        title = p['title']
        price = p['priceTag']['price']
        picture_url = p['image']['cropUrlTemplate']
        obj_list.append(Product(title, price, picture_url))

    return obj_list


def parse_product(product, query):
    headers_mobile = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B137 Safari/601.1'}

    obj_list = []
    url = f'https://www.perekrestok.ru/api/customer/1.4.1.0/catalog/search/all?textQuery={query}&entityTypes[]=product&entityTypes[]=category'
    response = requests.get(
        url, headers={'Authorization': f'Bearer {access_token}'})
    products = response.json()['content']['products']
    for p in products:
        if p['title'] == product:
            break
    obj_list.append(Shop('Перекрёсток', p['priceTag']['price']))
    picture_url = p['image']['cropUrlTemplate'].replace('%s', '400x400-fit')

    url = f'https://sbermegamarket.ru/catalog/?q={product}'

    r = requests.get(url)
    r.encoding = 'utf-8'
    text = BeautifulSoup(r.text, 'lxml')
    products = text.find_all(
        class_=re.compile('catalog-item ddl_product'))
    if len(products) > 0:
        href = products[0].find(class_=re.compile('ddl_product_link'))['href']
        href = "/".join(href.split('/')[:-1])
        needed_url = "https://sbermegamarket.ru" + href + "/#?details_block=prices"
        r_new = requests.get(needed_url, headers=headers_mobile)
        r_new.encoding = 'utf-8'
        product_data = BeautifulSoup(r_new.text, 'lxml')
        shops = product_data.find_all(
            'div', class_="product-offer")

        for shop in shops:
            title = re.search(r'([^-]+)', shop.find("a",
                                                    target=re.compile("_blank")).text).group(1)
            price = re.search(r'(\d+)', shop.find("span",
                                                  class_="product-offer-price__amount").text).group(1)
            obj_list.append(Shop(title, price))

    return obj_list, picture_url


def parse_structure(product, query):
    url = f'https://www.perekrestok.ru/api/customer/1.4.1.0/catalog/search/all?textQuery={query}&entityTypes[]=product&entityTypes[]=category'
    response = requests.get(
        url, headers={'Authorization': f'Bearer {access_token}'})

    products = response.json()['content']['products']
    for p in products:
        if p['title'] == product:
            break
    category_id = p['category']['id']
    slug = p['masterData']['slug']
    slug += '-' + p['masterData']['plu']
    product_url = f"https://www.perekrestok.ru/cat/{category_id}/p/{slug}"
    product_r = response = requests.get(
        product_url, headers={'Authorization': f'Bearer {access_token}'})
    data = BeautifulSoup(product_r.text, 'lxml')
    description = data.find(
        'pre', class_='product-composition-display-value')
    if not description:
        description = 'Отсутсвует'
    else:
        description = description.text
    structure = data.find('div', class_='sc-dlfnbm gfYllG')
    if not structure:
        structure = 'Отсутсвует'
    else:
        structure = structure.text
    return description, structure


if __name__ == '__main__':
    print(parse_structure('Coca Cola'))
