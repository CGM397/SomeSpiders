import requests
from bs4 import BeautifulSoup
import urllib
from urllib import request
from http import cookiejar


def login():
    login_info = {"email": "18805199056", "password": "123456"}
    cj = cookiejar.CookieJar()
    opener = request.build_opener(request.HTTPCookieProcessor(cj))
    req = request.Request('https://passport.meituan.com/account/unitivelogin', data=login_info)
    # response = opener.open(req)


def get_film_name_and_score(show_type, offset):
    params = {'showType': show_type, 'offset': offset}
    r = requests.get("https://maoyan.com/films", params=params)
    film_names = BeautifulSoup(r.content.decode(), 'lxml').find_all('div', class_="channel-detail movie-item-title")
    film_score = BeautifulSoup(r.content.decode(), 'lxml').find_all('div', class_="channel-detail channel-detail-orange")

    f = open("mao_yan_films.txt", "a", encoding="UTF-8")

    for index in range(len(film_names)):
        res = film_names[index]['title'] + "; 评分: "
        if film_score[index].string == '暂无评分':
            res += film_score[index].string
        else:
            res += film_score[index].contents[0].string + film_score[index].contents[1].string
        res += "\n"
        f.write(res)
    f.close()
    return
