import requests
from bs4 import BeautifulSoup
import random
import csv


def us_ag():
    with open('user_agent.txt', 'r', encoding='utf-8') as file:
        user_agent_list = []
        for i in file.readlines():
            user_agent_list.append({'user-agent': i.strip()})
    return user_agent_list


def soup(url, user_agent_list=us_ag()):
    response = requests.get(url, headers=random.choice(user_agent_list))
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'lxml')


def pages():
    default_url = 'https://www.novostroy37.ru'
    soup_parts = soup(default_url)
    c = False
    for part in soup_parts.find_all('li', class_='menu-item'):
        if not c:
            first = part
            c = True
        else:
            if part == first:
                break
        url_parts = f'{default_url}{part.find('a')['href']}'
        try:
            yield from [f'{url_parts}?PAGEN_1={i}' 
                        for i in range(1, 
                        int(soup(url_parts).find('div', class_='nums').find_all('a', class_='dark_link')[-1].text) + 1)]
        except AttributeError:
            continue


def in_stock():
    for url in pages():
        soup_stock = soup(url)
        for item in [(
            i.find('a', class_='dark_link').find('span').text.strip(),
            i.find('span', class_='value').text,
            f'https://novostroy37.ru{i.find('a', class_='dark_link')['href'].strip()}'
            )
            for i in soup_stock.find_all('div', class_='item_info TYPE_1')]:
            if item[1] == 'Нет в наличии':
                yield item


def writer():
    with open('out_of_stock.csv', 'w', newline='', encoding='utf-8-sig') as file:
        w = csv.writer(file, delimiter=';')
        w.writerow(['Наименование', 'Статус', 'Ссылка'])
        for i in in_stock():
            print(i)
            w.writerow([i[0], i[1], i[2]])


def main():
    writer()


if __name__ == '__main__':
    main()
