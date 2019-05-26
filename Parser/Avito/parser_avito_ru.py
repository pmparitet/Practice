import csv
import time
import random
import requests
from bs4 import BeautifulSoup as bs

# План:
# 1. Выяснить количество страниц
# 2. Сформировать список урлов на страницы выдачи
# 3. Собрать данные
# https://www.avito.ru/moskva/telefony?p=1&q=hts


def get_html(url, headers):
    """Получение HTML страницы"""
    session = requests.Session()
    request = session.get(url, headers=headers)
    if request.status_code == 200:
        print('Ответ сервера = {}'.format(request.status_code))
        return request.text
    else:
        print('Error! Ответ сервера = {}'.format(request.status_code))


def get_total_pages(html):
    """Функция получает и возвращает кол-во страниц для парсинга"""

    soup = bs(html, 'lxml')

    # фильтруем soup, берем последнюю строку кода и из неё ссылку на страницы рез. поиска
    pages = soup.find('div', class_='pagination-pages').find_all('a', attrs={'class': 'pagination-page'})[-1].get('href')

    # разделяем ссылку на элементы "=", получаем вротой эл. с номером стр.,
    # разделяем по аперанду и получем цифру страницы
    total_pages = pages.split('=')[1].split('&')[0]

    # меняем тип цыфры из строки на число (int), возвращаем цыфру во ВНЕ
    return int(total_pages)


def get_page_data(html):
    """Парсинг страницы и создание словаря с результатами"""
    soup = bs(html, 'lxml')

    ads = soup.find('div', class_='catalog-list').find_all('div', class_='item_table')

    # в цикле перебираем все обьявления
    for ad in ads:

        # в "name" и цикле проверяем есть в названии обьяления фраза "htc"
        name = ad.find('div', class_='description').find('h3').text.strip().lower()
        if 'htc' in name:

            try:
                # title = ad.find('a', attrs={'class': 'item-description-title-link'}).span.text
                title = ad.find('div', class_='description').find('h3').text.strip()
            except:
                title = ''

            try:
                url = 'https://www.avito.ru' + ad.find('div', class_='description').find('h3').find('a').get('href')
            except:
                url = ''

            try:
                price = ad.find('div', class_='about').text.strip()
            except:
                price = ''

            try:
                metro = ad.find('div', class_='data').find_all('p')[-1].text.strip()
            except:
                metro = ''

            data = {
                'title': title,
                'price': price,
                'metro': metro,
                'url': url
            }

            # вызов функции с записью в файл
            write_csv(data)
        else:
            continue


def write_csv(data):
    """Cохранение в csv файл"""
    with open('avito_HTC.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'],
                         data['price'],
                         data['metro'],
                         data['url']))


def main():
    """Основная функция"""
    headers = {'accept': '*/*',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/74.0.3729.157 Safari/537.36'}
    url = 'https://www.avito.ru/moskva/telefony?p=1&q=htc'
    base_url = 'https://www.avito.ru/moskva/telefony?'
    page_part = 'p='
    query_part = '&q=htc'

    # цикл генерирует url фикс кол-во страниц для парсинга
    for i in range(1, 2):
        url_gen = base_url + page_part + str(i) + query_part
        html = get_html(url_gen, headers)
        get_page_data(html)
        print('File save page {}, OK!'.format(i))
        time.sleep(random.random())

    # цикл генерирует url всех страниц для парсинга
    # total_pages = get_total_pages(get_html(url, headers))
    # for i in range(1, total_pages + 1):
    #     url_gen = base_url + page_part + str(i) + query_part
    #     html = get_html(url_gen, headers)
    #     get_page_data(html)
    #     print('File save page {}, OK!'.format(i))
    #     time.sleep(random.random()) # попытка обхода блокировки от сервера


if __name__ == '__main__':
    main()
