import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import date
import datetime
from bs4 import BeautifulSoup



driver = webdriver.Chrome('C:\Program Files\chromedriver.exe')

driver.get('https://www.amazon.com.au/')

search_bar = driver.find_element(By.XPATH, '//div[@class = "nav-search-field "]//input')
search_string = 'Apple Fast Charger'
search_bar.send_keys(search_string)

submit_button = driver.find_element(By.XPATH, '//div[@class = "nav-search-submit nav-sprite"]')
submit_button.click()

output = []

def scrape_page(driver):
    soup = BeautifulSoup(driver.page_source)
    time.sleep(2)
    items = soup.find_all('div', {'data-component-type': 's-search-result'})
    for r in items:
        
        scrape_box(r)
        

def scrape_box(box):
    dict = {}
    add_date(dict)
    add_title(box, dict)
    add_price(box, dict)
    add_reviews(box, dict)
    output.append(dict)

def add_date(dict):
    today = date.today()
    date_string = today.strftime("%Y-%m-%d")
    dict['Date'] = date_string


def add_title(box, output):
    container = box.h2.span
    title = container.text.strip()
    output['Title'] = title

def add_link(box, output):
    link = 'https://www.amazon.com.au/' + box.a['href']
    output['Link'] = link

def add_price(box, output):
    try:
        whole_number = box.find('span', {'class': 'a-price-whole'}).text.strip()
        decimal = box.find('span',{'class', 'a-price-fraction'}).text.strip()
        number = whole_number + '.' + decimal
        output['Price']  = (number)
    except:
        return

def add_reviews(box, output):
    try:
        no_reviews = box.find('span', {'class', 'a-size-base s-underline-text'}).text.strip()

        text = no_reviews.replace(",", '')
        output['Review Amount'] = int(text)
    except:
        return

    try:
        stars_text = box.find('span', {'class', 'a-icon-alt'}).text
        output['Review Score'] = stars_text.strip()
    except:
        return



def scrape_amazon(driver):
    scrape_page(driver)
    try:
        next_page(driver)
        time.sleep(5)
        scrape_amazon(driver)
    except:
        driver.close()
        return
    

def next_page(driver):
    pagination_body = driver.find_element(By.XPATH, '//span[@class = "s-pagination-strip"]')
    next = pagination_body.find_element(By.XPATH, './/a[text() = "Next"]')
    if next.get_property('class') == 's-pagination-item s-pagination-next s-pagination-disabled ':
        raise Exception
    else:
        next.click()


scrape_amazon(driver)

df = pd.DataFrame(output)
print(df)
    

    







