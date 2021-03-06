from bs4 import BeautifulSoup
from selenium import webdriver
import time
from spiders.maoyanSpider import dbConnector


def login_and_get_info():
    # 将Chrome驱动包放在Anaconda或者python的Scripts目录下
    driver = webdriver.Chrome()
    driver.get("https://passport.meituan.com/account/unitivelogin"
               "?service=maoyan&continue=https%3A%2F%2Fmaoyan.com%2Fpassport%2Flogin%3Fredirect%3D%252F")

    # 账号密码自行注册
    driver.find_element_by_name("email").send_keys("******")
    driver.find_element_by_name("password").send_keys("******")
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

    comments = open("film_comments.txt", "a", encoding="UTF-8")
    introductions = open("film_introduction.txt", "a", encoding="UTF-8")
    descriptions = open("film_description.txt", "a", encoding="UTF-8")
    directors = open("film_director.txt", "a", encoding="UTF-8")

    for film_name, film_href in film_id_hrefs.items():
        href = "https://maoyan.com" + film_href
        driver.get(href)

        save_comment(driver, comments, film_name)
        save_introduction(driver, introductions, film_name)
        save_description(driver, descriptions, film_name)
        save_director(driver, directors, film_name)

    comments.close()
    introductions.close()
    descriptions.close()
    directors.close()
    return


def save_comment(driver, comments, film_name):
    film_hot_comments = BeautifulSoup(driver.page_source, 'lxml').find_all('div', class_="comment-content")
    if film_hot_comments is None:
        comments.write(film_name + ": 暂无评价\n")
    else:
        for one_comment in film_hot_comments:
            comment_str = ""
            if one_comment.string is not None:
                comment_str = one_comment.string
            comment_str = comment_str.replace(' ', '')
            comment_str = comment_str.replace('\n', '')
            comments.write(film_name + ": " + comment_str + "\n")
    return


def save_introduction(driver, introductions, film_name):
    film_introductions = BeautifulSoup(driver.page_source, "lxml").find_all('li', class_='ellipsis')
    intro_type = ['类型', '时长', '上映时间']
    one_introduction = ""
    if film_introductions is not None:
        for index in range(len(film_introductions)):
            one_introduction += "\n  " + intro_type[index] + ": "
            intro_content = film_introductions[index].string
            if intro_content is None:
                one_introduction += "暂无"
            else:
                intro_content = intro_content.replace(' ', '')
                intro_content = intro_content.replace('\n', '')
                one_introduction += intro_content
    introductions.write(film_name + ":" + one_introduction + "\n")
    return


def save_description(driver, descriptions, film_name):
    film_description = BeautifulSoup(driver.page_source, "lxml").find('span', class_='dra')
    if film_description is None and film_description.string is not None:
        descriptions.write(film_name + ": 暂无剧情简介\n")
    else:
        descriptions.write(film_name + ": " + film_description.string + "\n")
    return


def save_director(driver, directors, film_name):
    film_director = BeautifulSoup(driver.page_source, 'lxml').find('div', class_="celebrity-type")
    director_str = ""
    if film_director is not None and film_director.string is not None:
        director_str = film_director.string
    director_str = director_str.replace(' ', '')
    director_str = director_str.replace('\n', '')
    res = film_name + " 导演: "
    if director_str == "导演":
        # film_director.next_sibling is ""
        name_lists = film_director.next_sibling.next_sibling
        names = name_lists.find_all('a', class_='name')
        for one_name in names:
            name_str = one_name.string
            name_str = name_str.replace(' ', '')
            name_str = name_str.replace('\n', '')
            res += name_str + "; "
    else:
        res += "暂无"
    directors.write(res + "\n")
    return


def save_to_db():
    save_info_to_db()
    save_description_to_db()
    save_comments_to_db()
    return


def save_info_to_db():
    introduction = open("film_introduction.txt", "r", encoding="UTF-8")
    director = open("film_director.txt", "r", encoding="UTF-8")
    score = open("mao_yan_films.txt", "r", encoding="UTF-8")
    introductions = introduction.readlines()
    directors = director.readlines()
    scores = score.readlines()

    one_film_name = ""
    one_film_type = ""
    one_filming_location = ""
    one_film_duration = ""
    for index in range(len(introductions)):
        one_introduction_line = introductions[index]
        if index % 4 == 0:
            one_film_name = one_introduction_line[:-2]
        elif index % 4 == 1:
            one_film_type = one_introduction_line[one_introduction_line.find(': ') + 2:-1]
        elif index % 4 == 2:
            if one_introduction_line.find('/') != -1:
                one_filming_location = one_introduction_line[
                                one_introduction_line.find(': ') + 2:one_introduction_line.find('/')]
                one_film_duration = one_introduction_line[one_introduction_line.find('/') + 1:-1]
            else:
                one_filming_location = one_introduction_line[one_introduction_line.find(': ') + 2:-1]
                if one_filming_location == "":
                    one_filming_location = "暂无"
                one_film_duration = "暂无"
        elif index % 4 == 3:
            one_film_released_time = one_introduction_line[one_introduction_line.find(': ') + 2:-1]
            one_director_line = directors[int(index/4)]
            one_film_director = one_director_line[one_director_line.find(': ') + 2:-2]
            print(one_film_director)
            if one_film_director == '暂':
                one_film_director = "暂无"
            else:
                one_film_director = one_film_director[:-1]
            print("after" + one_film_director)
            one_film_score = scores[int(index/4)][scores[int(index/4)].find(': ') + 2:-1]
            dbConnector.insert_film_info(int(index/4), one_film_name, one_film_director, one_film_type,
                                         one_filming_location, one_film_duration, one_film_released_time,
                                         one_film_score)
    introduction.close()
    director.close()
    score.close()
    return


def save_description_to_db():
    description = open("film_description.txt", "r", encoding="UTF-8")
    lists = description.readlines()
    description_id = 0
    for one in lists:
        if one is not None and one.__len__() > 0:
            film_name = one[:one.find(': ')]
            film_description = one[one.find(': ') + 2:-1]
            dbConnector.insert_film_description(description_id, film_name, film_description)
        description_id += 1
    description.close()
    return


def save_comments_to_db():
    comment = open("film_comments.txt", "r", encoding="UTF-8")
    lists = comment.readlines()
    comment_id = 0
    for one in lists:
        if one is not None and one.__len__() > 0:
            film_name = one[:one.find(': ')]
            film_comment = one[one.find(': ') + 2:-1]
            dbConnector.insert_film_comment(comment_id, film_name, film_comment)
        comment_id += 1
    comment.close()
    return


"""
def get_film_name_and_score(show_type, offset):
    params = {'showType': show_type, 'offset': offset}
    r = requests.get("https://maoyan.com/films", params=params)
    film_names = BeautifulSoup(r.content.decode(), 'lxml').find_all('div', 
                            class_="channel-detail movie-item-title")
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
"""