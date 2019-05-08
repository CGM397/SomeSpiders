import requests
from bs4 import BeautifulSoup

web_url = 'https://unsplash.com'
r = requests.get(web_url)
all_a = BeautifulSoup(r.text, 'lxml').find_all('img', class_='_2zEKz')

for a in all_a:
    print(a)
