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
    film_id_hrefs = {}

# get film name and score

    f = open("mao_yan_films.txt", "a", encoding="UTF-8")
    for index in range(len(film_names)):
        one_name = film_names[index]['title']
        res = one_name + "; 评分: "
        film_id_hrefs[one_name] = film_names[index].contents[1]["href"]
        if film_score[index].string == '暂无评分':
            res += film_score[index].string
        else:
            res += film_score[index].contents[0].string + film_score[index].contents[1].string
        res += "\n"
        f.write(res)
    f.close()

# get other film info like comment and introduction and description
    save_comments = open("film_comments.txt", "a", encoding="UTF-8")
    save_introduction = open("film_introduction.txt", "a", encoding="UTF-8")
    save_description = open("film_description.txt", "a", encoding="UTF-8")

    for film_name, film_href in film_id_hrefs.items():
        href = "https://maoyan.com" + film_href
        driver.get(href)
        film_hot_comment = BeautifulSoup(driver.page_source, 'lxml').find('div', class_="comment-content")
        if film_hot_comment is None:
            save_comments.write(film_name + ": 暂无评价\n")
        else:
            save_comments.write(film_name + ": " + film_hot_comment.string + "\n")

        film_introductions = BeautifulSoup(driver.page_source, "lxml").find_all('li', class_='ellipsis')
        intro_type = ['类型', '时长', '上映时间']
        one_introduction = ""
        for index in range(len(film_introductions)):
            one_introduction += " " + intro_type[index] + ": "
            intro_content = film_introductions[index].string
            if intro_content is None:
                one_introduction += "暂无"
            else:
                one_introduction += intro_content
        save_introduction.write(film_name + ":" + one_introduction + "\n")

        film_description = BeautifulSoup(driver.page_source, "lxml").find('span', class_='dra')
        if film_description == '':
            save_description.write(film_name + ": 暂无简介\n")
        else:
            save_description.write(film_name + ": " + film_description.string + "\n")

    save_comments.close()
    save_introduction.close()
    save_description.close()
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
