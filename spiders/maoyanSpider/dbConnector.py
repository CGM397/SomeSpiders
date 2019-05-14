import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='maoYanFilm',
                             charset='UTF8MB4',
                             cursorclass=pymysql.cursors.DictCursor)


def insert_film_info(info_id, film_name, film_director, film_type,
                     filming_location, film_duration, film_released_time, film_score):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `filmInfo`(`id`, `name`, `director`, `type`, `filmingLocation`," \
              " `duration`,  `releasedTime`, `score`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (info_id, film_name, film_director, film_type,
                             filming_location, film_duration, film_released_time, film_score))
    connection.commit()


def insert_film_comment(comment_id, film_name, film_comment):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `filmComment`(`id`, `filmName`, `comment`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (comment_id, film_name, film_comment))
    connection.commit()


def insert_film_description(description_id, film_name, film_description):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `filmDescription`(`id`, `filmName`, `description`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (description_id, film_name, film_description))
    connection.commit()
