# coding=utf-8
import csv
from datetime import datetime, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import sys,time

def get_number(html):
    soup = BeautifulSoup(html,'html.parser')
    name = soup.find('div', class_='_0 _25 _2p _2 _6i _6k _h')
    ty = name.find_all('div', class_='_0 _25 _2p _6m')
    i = 0
    for t in ty:
        i += 1
        b = t
    if i > 3:
        number = b.find('div',class_='_su _st _sv _sm _5k _sn _sr _nl _nm _nn _no').text.encode('utf-8')
        if 'k' in number:
            number = number.replace('k', '')
            number = number.replace(',', '.')
            num = float(number)
            num = num * 1000
        else:
            num = float(number)
        try:
            num = int(num)
        except Exception:
            pass
        number = num + 3
    else:
        number = i
    return number


def main():
    start = datetime.now()
    username = raw_input('Please enter your username ')
    username = str(username)
    password_u = raw_input('Please enter your password ')
    password_u = str(password_u)
    word = raw_input('What will you look for? ')
    word = str(word)
    brd = raw_input('How many boards do you need? ')
    brd = int(brd)
    ######  Page wait time. It is necessary to ensure that it is not banned
    sleep_time = 3
    ######
    browser = webdriver.Firefox()
    browser.get('https://pinterest.com/login')
    time.sleep(sleep_time)

    user=browser.find_element_by_name('id')
    user.send_keys(username)
    password = browser.find_element_by_name('password')
    password.send_keys(password_u)
    login = browser.find_element_by_css_selector('.red')
    login.click()
    time.sleep(sleep_time)
    browser.get('https://pinterest.com/search/boards/?q='+word)
    htm = browser.find_element_by_class_name('SearchPageContent')
    # Scrolls the page to load more boards.
    for i in range(10000):
        try:
            htm.send_keys(Keys.PAGE_DOWN)
        except ElementNotInteractableException:
            pass

    boards = browser.find_elements_by_class_name('boardLinkWrapper')
    links = []
    names = []
    pins = []
    followers = []
    desc = []
    group_members = []
    i = 0
    # Adds all the references to the boards according to your request in a variable.
    # !!! This can take a few minutes if you need 1000 boards. !!!
    for k in range(brd):
        links.append(boards[k].get_attribute('href').encode('utf-8'))
    for link in links:
        browser.get(link)
        time.sleep(sleep_time)
        n = browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div[3]'
                                             '/div/div[2]/div[1]/div[2]/div/div[1]/h3').text
        names.append(n.encode('utf-8'))
        p = browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div[3]'
                                             '/div/div[2]/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/span[1]').text
        pins.append(p.encode('utf-8'))
        f = browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div[3]/div/div[2]'
                                                      '/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/button/span[1]').text
        followers.append(f.encode('utf-8'))
        # try:
        check = browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]'
                                                  '/div[3]/div/div[2]/div[1]/div[2]/div/'
                                                  'div[2]/div/div[1]/div[3]/div').text
        if check:
            desc.append(check.encode('utf-8'))
        else:
            desc.append('None')
        html = browser.page_source
        count = get_number(html)
        group_members.append(count)
        print 'Board number', i+1, 'is done.'
        i += 1
        browser.back()
        time.sleep(sleep_time)
        if i == brd:
            break
    # Opens the file and writes new information into it.
    # If there is already information in it, it writes down half of it
    with open( 'boards\\' + word + '.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(('Board Url','Board Name','Pins','Followers','Groupb Board Members','Board Description'))
        for i in range(len(names)):
            writer.writerow( (links[i],names[i],pins[i],followers[i],group_members[i],desc[i]) )
    end = datetime.now()
    total = end - start
    print 'Operating time: ', total


if __name__ == '__main__':
    main()
