import requests
import time
import csv


def take_1000_posts():
    """Функция парсит 1000 постов и записывает в список 'all_post'."""

    token = '64774e6764774e6764774e6781641d8a0e6647764774e67389e143fe98e964427a24577'
    version = 5.92
    domain = 'fit4life_official'

    # кол-во постов для отображения
    count = 100

    # "offset" смещение, необходимое для выборки определенного подмножества записей,
    # когда спарсили первые 100 постов прибавляем для начала отсчета 101-200 и т.д.
    offset = 0
    all_post = []

    # в цикле можно установить какое кол-во постов нужно
    while offset < 1000:
        response = requests.get('https://api.vk.com/method/wall.get',
                                params={
                                    'access_token': token,
                                    'v': version,
                                    'domain': domain,
                                    'count': count,
                                    'offset': offset
                                })
        data = response.json()['response']['items']
        offset += 100

        # Расширяет список [], добавляя в конец все элементы списка "data"
        all_post.extend(data)
        time.sleep(0.5)
    return all_post


def post_content_filter(all_posts):
    """Фильтр, для получения полей: 'likes', 'text', 'img_url'."""

    post_filter = []
    for post in all_posts:
        # получаем url картинки
        try:
            if post['attachments'][0]['type']:
                img_url = post['attachments'][0]['photo']['sizes'][-1]['url']
            else:
                img_url = 'pass'
        except:
            pass

        post_filter.append({
            'likes': post['likes']['count'],
            'text': post['text'],
            'img_url': img_url
            })
    return post_filter


def file_writer(data):
    """Запись в файл: кол-во лайков, тело поста, url картинки поста"""

    with open('fit4life.csv', 'w', encoding='utf-8', newline='') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('likes', 'body', 'url'))
        for post in data:
            a_pen.writerow((post['likes'], post['text'], post['img_url']))


all_posts = take_1000_posts()

# печать в терминал отфильтрованных данных
print(post_content_filter(all_posts))

# запись отфильтрованных данных в файл
# post_filter = post_content_filter(all_posts)
# file_writer(post_filter)
