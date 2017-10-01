import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing import Pool



def get_html(url):
    r = requests.get(url)
    return r.text  # return html


def get_all_links(html):
    soup = BeautifulSoup(html,'lxml')
    countys = soup.find('ul', id='statelist').find_all('li')
    links = []
    name = []
    for count in countys:
        link ='http://www.county-clerk.net/' + count.find('a').get('href')
        county = count.text
        links.append(link)
        name.append(county)
    return name, links


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        content = soup.find('div', class_='content')
        data = content.find_all('div',class_='info')
        adress = str(data[0].text)
        phone = data[1].text
        return adress, phone
    except Exception:
        return None


def write_csv(data):
    with open('olkahoma.csv','a') as f:
        writer = csv.writer(f)
        writer.writerow((data['name'],data['address'],data['phone']))


def make_all(link, name):
    adress, phone = (get_page_data(get_html(link)))
    new_adr = adress.replace('\t', '').replace('\r', '').replace('\n', '').lstrip()
    new_phone = phone.replace('\t', '').replace('\r', '').replace(' ', '').replace('\n', '')
    data = {'name': name,
            'address': new_adr,
            'phone': new_phone}
    write_csv(data)
    print(data)

def main():
    # 46 sec parsing
    start = datetime.now()
    url = 'http://www.county-clerk.net/county.asp?state=Oklahoma'
    html = get_html(url)
    names,links = get_all_links(html)
    i = 0
    for i in range(len(links)):
        adress, phone = (get_page_data(get_html(links[i])))
        new_adr = adress.replace('\t','').replace('\r','').replace('\n','').lstrip()
        new_phone = phone.replace('\t','').replace('\r','').replace(' ', '').replace('\n','')
        data = {'name': names[i],
                'address': new_adr,
                'phone': new_phone }
        write_csv(data)
        print(data)
    # for multipocessing
    # with Pool(40) as p:
    #     p.map(make_all, links)
    end = datetime.now()
    total = end - start
    print(total)

if __name__ == '__main__':
    main()