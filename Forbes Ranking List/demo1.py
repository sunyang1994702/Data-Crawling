
"""This is a simple expamle for crawling the forbeschina website."""

from bs4 import BeautifulSoup
import requests
import csv


def get_data(url):
    req = requests.get(url)
    bf = BeautifulSoup(req.text)
    return bf.find_all('tr')


def save_data(items):
    results = []
    results.append([i.text for i in items[0].find_all('th')])
    for item in items[1:-1]:
        results.append([i.text for i in item.find_all('td')])

    with open("2020_forbes_list.csv", 'a+', newline='', encoding='utf-8-sig') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(results)


if __name__ == '__main__':
    url = "https://www.forbeschina.com/lists/1733"
    items = get_data(url)
    save_data(items)