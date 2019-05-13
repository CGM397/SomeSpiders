import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='maoYanFilm',
                             charset='UTF8MB4',
                             cursorclass=pymysql.cursors.DictCursor)

