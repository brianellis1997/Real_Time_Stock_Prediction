import pandas as pd
import datetime
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

def web_content_div(web_content, class_path):
    web_content_div = web_content.find_all('div', {'class': class_path})
    try:
        spans = web_content_div[0].find_all('span')
        texts = [span.get_text() for span in spans]
    except IndexError:
        texts = []
    return texts

def real_time_price(stock_code):
    url = 'https://finance.yahoo.com/quote/' + stock_code
    try:
        r = requests.get(url)
        web_content = BeautifulSoup(r.text, 'lxml')
        texts = web_content_div(web_content, 'container yf-aay0dk')
        if texts != []:
            price, change = texts[0], texts[1]
        else:
            price, change = [], []
    
        texts = web_content_div(web_content, 'container yf-tx3nkj')
        if texts != []:
            for count, vol in enumerate(texts):
                if vol == 'Volume':
                    volume = texts[count + 1]
        else:
            volume = []

        pattern = web_content_div(web_content, 'Fz(xs) Mb(4px)')
        try:
            latest_pattern = pattern[0]
        except IndexError:
            latest_pattern = []

        texts = web_content_div(web_content, 'container yf-tx3nkj')
        if texts != []:
            for count, target, in enumerate(texts):
                if target == '1y Target Est':
                    one_year_target = texts[count + 1]
        else:
            one_year_target = []
    
    except ConnectionError:
        price, change, volume, latest_pattern, one_year_target = [], [], [], [], []
    return price, change, volume, latest_pattern, one_year_target


Stock = ['BRK-B']
print(real_time_price('BRK-B'))