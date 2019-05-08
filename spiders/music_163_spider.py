import requests
from bs4 import BeautifulSoup

params = {'id': 2002, 'initial': 65}
r = requests.get("https://music.163.com/discover/artist/cat", params=params)
artists = BeautifulSoup(r.content.decode(), 'lxml').find_all('a', class_="nm nm-icn f-thide s-fc0")

for artist in artists:
    print(artist['href'].replace('/artist?id=', '').strip(), artist['title'].replace('的音乐', ''))
