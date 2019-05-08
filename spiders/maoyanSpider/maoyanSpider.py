from spiders.maoyanSpider.getFilmNameAndScore import get_film_name_and_score, login

# login()
for i in range(0, 27892):
    get_film_name_and_score("3", i * 30)
