import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time


def login_and_get_info():
    driver = webdriver.Chrome()
    driver.get("https://passport.meituan.com/account/unitivelogin"
               "?service=maoyan&continue=https%3A%2F%2Fmaoyan.com%2Fpassport%2Flogin%3Fredirect%3D%252F")

    driver.find_element_by_name("email").send_keys("18805199056")
    driver.find_element_by_name("password").send_keys("123456cgm")
    driver.find_element_by_name("commit").click()

    time.sleep(3)
    driver.save_screenshot("maoyan.png")
    for i in range(0, 66):
        get_info(driver, "3", i * 30)


def get_info(driver, show_type, offset):
    driver.get("https://maoyan.com/films?showType=" + show_type + "&offset=" + str(offset))
    film_names = BeautifulSoup(driver.page_source, 'lxml').find_all('div',
                                                                    class_="channel-detail movie-item-title")
    film_score = BeautifulSoup(driver.page_source, 'lxml').find_all('div',
                                                                    class_="channel-detail channel-detail-orange")
    film_id_hrefs = []

    f = open("mao_yan_films.txt", "a", encoding="UTF-8")

    for index in range(len(film_names)):
        res = film_names[index]['title'] + "; 评分: "
        film_id_hrefs.append(film_names[index].contents[1]["href"])
        if film_score[index].string == '暂无评分':
            res += film_score[index].string
        else:
            res += film_score[index].contents[0].string + film_score[index].contents[1].string
        res += "\n"
        f.write(res)
    f.close()
    print(film_id_hrefs[0])
    return


def get_film_name_and_score(show_type, offset):
    params = {'showType': show_type, 'offset': offset}
    r = requests.get("https://maoyan.com/films", params=params)
    film_names = BeautifulSoup(r.content.decode(), 'lxml').find_all('div', class_="channel-detail movie-item-title")
    film_score = BeautifulSoup(r.content.decode(), 'lxml').find_all('div',
                                                                    class_="channel-detail channel-detail-orange")

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
