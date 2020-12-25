from bs4 import BeautifulSoup
import csv
import requests

from url import URL


def _get_link(url=URL):
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def _make_soup():
    soup = BeautifulSoup(_get_link(), 'html.parser')
    return soup


def _get_rate(soup):
    table = soup.find('table', class_='table-resp')
    rows = table.find_all('tr')
    return rows[3].find('td').text


def _get_lowest():
    with open('rates.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        lowest = min([row for row in reader])[0]
    return lowest


def write_rate(rate):
    with open('rates.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([rate])


if __name__ == '__main__':
    soup = _make_soup()
    today = _get_rate(soup)
    low = _get_lowest()
    write_rate(today)

    if today < low:
        print(f'{today} v')
    elif today > low:
        print(f'{today} ^')
    else:
        print(f'{today} -')
