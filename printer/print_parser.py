import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing import Pool



def get_html_and_register(url, name):
    s = requests.Session()
    response = s.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    # for n in soup('input'):
    #     if n['name'] == '_csrf_token':
    #         token = n['value']
    #         break
    auth = {
        'id': 'i4570i@rambler.ru',
        'password': 'q1w2e3r4t5y6'
        # '_csrf_token': token
    }
    s.post(url, data=auth)
    response = s.get(url + name)
    return response.text # return html


def get_all_links(html):
    soup = BeautifulSoup(html,'lxml')
    county = soup.find_all('div', class_='cardWrapper')
    link = []
    for coun in county:
        link.append('https://ru.pinterest.com' + coun.find('a').get('href'))

    return link




def main():
    # 46 sec parsing
    start = datetime.now()
    url = 'https://ru.pinterest.com/'
    name = 'kim_96/'
    html = get_html_and_register(url,name)
    link = get_all_links(html)
    for l in link:
        print(l)



    # for multipocessing
    # with Pool(40) as p:
    #     p.map(make_all, links)
    end = datetime.now()
    total = end - start
    print(total)

if __name__ == '__main__':
    main()