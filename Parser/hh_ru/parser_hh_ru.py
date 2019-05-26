import csv
import requests
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/74.0.3729.157 Safari/537.36'}

base_url = 'https://hh.ru/search/vacancy?order_by=publication_time&clusters=true&area=1&' \
           'text=Python&enable_snippets=true&search_period=3&page=0'


def hh_parse(base_url, headers):
    """Парсит данные, и записывает в список 'jobs'."""
    jobs = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:

        request = session.get(base_url, headers=headers)
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f'https://hh.ru/search/vacancy?order_by=publication_time&clusters=true&area=1&text=Python' \
                    f'&enable_snippets=true&search_period=3&page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass

    for url in urls:
        request = session.get(url, headers=headers)
        soup = bs(request.content, 'lxml')
        divs_ost = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
        divs_premium = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy vacancy-serp__vacancy_premium'})
        divs = divs_premium + divs_ost

        for div in divs:
            try:
                title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                text1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                text2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                content = text1 + ' ' + text2

                jobs.append({
                    'title': title,
                    'href': href,
                    'company': company,
                    'content': content
                })
            except:
                pass
        print(len(jobs))
    else:
        print('ERROR or Done. Status_code = {0}'.format(request.status_code))
    return jobs


def files_writer(jobs):
    """Запись файла с кодировкой UTF-8"""
    with open('parsed_jobs.csv', 'w', encoding='utf-8', newline='') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('Название вакансии', 'URL', 'Название компании', 'Описание'))
        for job in jobs:
            a_pen.writerow((job['title'], job['href'], job['company'], job['content']))
        print('File save, OK!')


# чтение файла
# with open('parsed_jobs.csv', encoding='utf-8') as f:
#     print(f.read())


# выводит данные в консоль без сохранения в файле
print(hh_parse(base_url, headers))

# записывает данные в файл
# jobs = hh_parse(base_url, headers)
# files_writer(jobs)
