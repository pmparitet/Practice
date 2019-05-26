# Функция парсит таблицу на сайте http://malvina-club.ru/hours/
# при работе по умолчанию печатает список в терминал
# можно настроить вывод и передачу в списке одной строкой
# или "списка в списке"(но полько после дней строки, т.к. словарь перезаписывается хз как решить это)


import requests
from bs4 import BeautifulSoup as bs


headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/74.0.3729.157 Safari/537.36'}

b_url = 'http://malvina-club.ru/hours/'


def girl_pars():
    # data = {}
    session = requests.Session()
    request = session.get(b_url, headers=headers)

    if request.status_code == 200:

        soup = bs(request.content, 'lxml')
        hours_table = soup.find('table', attrs={'id': 'hours_table'})
        girls_info = hours_table.find_all('tr', attrs={'class': 'hours'})

        for girl in girls_info:
            hours = [x['data-hours'] for x in girl.find_all("td", {'data-rest': 'false'})]
            date = [x['data-date'] for x in girl.find_all("td", {'data-rest': 'false'})]
            data_rest = [x.text for x in girl.find_all("td", {'data-rest': 'true'})]
            work_time = dict(zip(date, hours))

# создается словарь, если смотреть за цикл, то он каждый раз перезаписывается
# избежать этого можно записав получаемые значения в список "data.append(<словарь для записи>)"
# для этого создаем чистый список "data = []" в верху функции
# и через "return data" передаем его во ВНЕ для дальнейшей работы с ним
            data = {
                    'name': girl.span.text,
                    'girl_id': girl.a['data-id'],
                    'work_time': work_time,
                    'data_rest': data_rest,
                    'foto': girl.img['src']
            }
            print(data)

# вложеная структура словаря {'name':{'Алина':{'girl_id': '2443', 'work_time': {}, 'data_rest': ['В отпуске до 5 июня'],
#                                              'foto': 'http://malvina}}}

            # data.update({
            #     'name': {
            #         girl.span.text: {
            #             'girl_id': girl.a['data-id'],
            #             'work_time': work_time,
            #             'data_rest': data_rest,
            #             'foto': girl.img['src']
            #         }
            #     }
            # })
            # print(data)

# возвращает значение
    # return data


girl_pars()

# для получения значений при использовании return
# print(girl_pars())
