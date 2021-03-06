import sqlite3
from collections import Counter


class DbConnect:
    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def __del__(self):
        self.cur.close()
        self.con.close()


# def exec_query(query, path='netflix.db'):
#     with sqlite3.connect(path) as con:
#         cur = con.cursor()
#         cur.execute(query)
#         result = cur.fetchone()
#     return result
#
#
# def movie_by_title2(title):
#     query = f"""select title, country, release_year, listed_in, description
#                 from netflix
#                 where title like '%{title}%'
#                 order by  release_year desc
#                 limit 100"""
#     result = exec_query(query)
#     return {
#         "title": result[0],
#         "country": result[1],
#         "release_year": result[2],
#         "genre": result[3],
#         "description": result[4]
#     }


def movie_by_title(title):
    """Поиск фильма по названию"""
    db_connect = DbConnect('netflix.db')
    query = f"""select title, country, release_year, listed_in, description
                from netflix
                where title like '%{title}%'
                order by  release_year 
                desc limit 1"""
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchone()
    return {
        "title": result[0],
        "country": result[1],
        "release_year": result[2],
        "genre": result[3],
        "description": result[4]
    }


def movies_between_years(year1, year2):
    """Поиск фильма по диапазону лет"""
    db_connect = DbConnect('netflix.db')
    query = f"""select title, release_year
                from netflix
                where release_year between {year1} and {year2}
                limit 100"""
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0],
                            "release_year": movie[1]})
    return result_list


def movies_by_rating(rating):
    """Поиск фильма по группе/категории"""
    rating_entities = {  # Перечень возможных групп/категорий по заданию "домашки"
        "children": "'G'",
        "family": "'G', 'PG', 'PG-13'",
        "adult": "'R', 'NC-17'"
    }
    if rating not in rating_entities:
        return "Выбранной Вами группы/категории не представлено"
    db_connect = DbConnect('netflix.db')
    query = f"""select title, rating, description
                from netflix
                where rating in ({rating_entities[rating]})"""
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0],
                            "rating": movie[1],
                            "description": movie[2]})
    return result_list


def movies_by_genre(genre):
    """Поиск фильма по жанру"""
    db_connect = DbConnect('netflix.db')
    query = f"""select title, description
                from netflix
                where listed_in like '%{genre}%'
                order by release_year desc
                limit 10"""
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0],
                            "description": movie[1]})
    return result_list


def actors_colleagues(actor1, actor2):
    """Поиск актеров-коллег, которые играли больше 2х раз вместе с АКТЕРОМ1 и АКТЕРОМ2"""
    db_connect = DbConnect('netflix.db')
    query = f"""select `cast` 
                from netflix  
                where `cast` like '%{actor1}%' 
                and `cast` like '%{actor2}%'"""
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()  # Список актеров по фильмам

    colleagues = []  # Общий список актеров из всех фильмов
    for cast in result:
        colleagues.extend(cast[0].split(', '))

    count = Counter(colleagues)
    colleagues_checklist = []  # Список актеров, игравших в более чем 2х фильмах вместе
    for actor, count in count.items():
        if actor not in [actor1, actor2] and count > 2:
            colleagues_checklist.append(actor)
    return colleagues_checklist


def movies_by_params(typ, release_year, listed_in):
    """Поиск фильма по параметрам: тип, год выхода, жанр"""
    db_connect = DbConnect('netflix.db')
    query = f"""SELECT title, description
                  from netflix
                  where type = '{typ}' and release_year = {release_year} and listed_in like '%{listed_in}%'"""
    db_connect.cur.execute(query)
    result = db_connect.cur.fetchall()
    result_list = []
    for movie in result:
        result_list.append({"title": movie[0],
                            "description": movie[1]})
    return result_list


