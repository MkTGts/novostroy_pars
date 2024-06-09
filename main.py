import requests
from bs4 import BeautifulSoup
import random
import time



with open('user_agent.txt', 'r', encoding='utf-8') as file:
    user_agent_list = []
    for i in file.readlines():
        user_agent_list.append({'user-agent': i.strip()})
    #print(*user_agent_list, sep='\n')



def soup(url):
    response = requests.get(url, headers=random.choice(user_agent_list))
    response.encoding = 'utf-8'
    return BeautifulSoup(response.text, 'lxml')


def pages():
    default_url = 'https://www.novostroy37.ru'
    soup_parts = soup(default_url)
    for part in soup_parts.find_all('li', class_='menu-item'):
        url_parts = f'{default_url}{part.find('a')['href']}'
        try:
            yield from [f'{url_parts}?PAGEN_1={i}' 
                        for i in range(1, 
                        int(soup(url_parts).find('div', class_='nums').find_all('a', class_='dark_link')[-1].text) + 1)]
        except AttributeError:
            continue
        

        



def main():
    d = {}
    for i in pages():
        print(i)
        s = requests.get(i, headers=random.choice(user_agent_list))
        if s.status_code != 200:
            d[i] = d.get(i, s.status_code)
            print(d[i])
            time.sleep(20)
            s2 = requests.get(i, headers=random.choice, timeout=30)
            print(f'new status = {s2.status_code}')

    print(d)


if __name__ == '__main__':
    main()
