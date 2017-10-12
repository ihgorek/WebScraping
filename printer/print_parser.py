# coding=utf-8
import mechanize
import requests
from mechanize import Browser
from bs4 import BeautifulSoup
from datetime import datetime, time
import sys

# LOGIN_URL = 'https://ru.pinterest.com/'
# SEARCH_URL = 'https://ru.pinterest.com/'
# ID = 'i4570i@rambler.ru',
# PASSWORD = 'q1w2e3r4t5y6'
# USERS = ['kim_96/','i4570i/']
#
# def fetch():
#     result_no = 0  # количество файлов с результатами
#     br = Browser()  # создаем браузер
#     br.open(LOGIN_URL)  # открываем страницу входа на сайт
#     br.select_form (name="id")  # находим форму для ввода имени и пароля
#     br['id'] = ID  # заполняем форму
#     br['password'] = PASSWORD
#     resp = br.submit()
#     # Автоматическое перенаправление иногда не срабатывает, поэтому
#     # при необходимости переходим вручную
#     if 'Redirecting' in br.title():
#         resp = br.follow_link(text_regex='click here')
#
#     # Обходим результаты поиска, сохраняя значения постоянных параметров
#     for user in USERS:
#         # Мне нравится видеть в консоли, что делает скрипт
#         print >> sys.stderr, '***', user
#         # Выполняем запрос
#         br.open(SEARCH_URL + user)
#         # Запрос выдает нам ссылки на страницы с нужными нам данными
#         # но на странице имеются и ненужные ссылки, которые мы будем игнорировать
#         nice_links = [l for l in br.links()
#                       if 'good_path' in l.url
#                       and 'credential' in l.url]
#         if not nice_links:  # Возможно, что не окажется никаких результатов
#             break
#         for link in nice_links:
#             try:
#                 response = br.follow_link(link)
#                 # Пишем в консоль заголовок страницы, на которую мы переходим
#                 print >> sys.stderr, br.title()
#                 # инкрементируем номер в имени файла, открываем файл и записываем
#                 # в него результат
#                 result_no += 1
#                 out = open('result' + {1}.format(result_no), 'w')
#                 print >> out, response.read()
#                 out.close()
#                 # Конечно, иногда могут случаться ошибки, мы будем их игнорировать
#             except mechanize._response.httperror_seek_wrapper:
#                 print >> sys.stderr, "Response error (probably 404)"
#             # Не будем напрягать сайт слишком частыми запросами
#             time.sleep(1)

def get_html_and_register(url):
    response = requests.get(url)
    return response.text # return html


def get_all_links(html):
    soup = BeautifulSoup(html,'lxml')
    county = soup.find_all('div', class_='_3wC7P')
    link = []
    name = []
    pins = []
    for coun in county:
        link.append('https://ru.pinterest.com' + coun.find('a').get('href'))
        name.append(coun.find('div', class_='boardName').find('div', class_='name').text)
        pins.append(coun.find('div', class_='boardName').find('div', class_='boardPinCount').text)
    return link,name,pins

def main():
    # 46 sec parsing
    start = datetime.now()
    url = 'https://ru.pinterest.com/kim_96/'
    html = get_html_and_register(url)
    links,names,pins = get_all_links(html)
    for i in range(len(links)):
        print links[i],' -> ',names[i], ' --> ', pins[i]
    end = datetime.now()
    total = end - start
    print(total)


if __name__ == '__main__':
    main()