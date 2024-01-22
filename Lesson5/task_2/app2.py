# Задание №2
# - Создать API для получения списка фильмов по жанру. Приложение должно
#   иметь возможность получать список фильмов по заданному жанру.
# - Создайте модуль приложения и настройте сервер и маршрутизацию.
# - Создайте класс Movie с полями id, title, description и genre.
# - Создайте список movies для хранения фильмов.
# - Создайте маршрут для получения списка фильмов по жанру (метод GET).
# - Реализуйте валидацию данных запроса и ответа.


import logging

from fastapi import FastAPI

from Lesson5.task_2.models import MoviesBase, Movies, Base, engine, db2

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app2 = FastAPI()


@app2.get("/movies")
async def read_root():
    res = []
    logger.info('Отработал GET запрос.')
    movies = db2.query(MoviesBase).all()
    for movie in movies:
        res.append(
            f"  movie_id: {movie.movie_id}, title: {movie.title},"
            f" description: {movie.description}, genre: {movie.genre}  ")
    return res


@app2.get("/movies/{genre}")
async def read_root(genre: str):
    res = []
    logger.info('Отработал GET запрос.')
    movies = db2.query(MoviesBase).filter(MoviesBase.genre == genre).all()
    for movie in movies:
        res.append([movie.movie_id, movie.title])
    return f"Movie list:  movies: {res}"


@app2.post("/movies/{movie_id}")
async def create_item(movie_id: int, movie: Movies):
    logger.info('Отработал POST запрос.')
    movies = db2.query(MoviesBase).filter(
        MoviesBase.movie_id == movie_id).all()
    for movie in movies:
        if movie.movie_id == movie_id:
            return f'Movie already exist!'
    else:
        movie = MoviesBase(movie_id=movie.movie_id, title=movie.title,
                           description=movie.description, genre=movie.genre,
                           is_del=False)
        db2.add(movie)
        db2.commit()
        return f"Movie:  movie_id: {movie.movie_id}, title: {movie.title}," \
            f" description: {movie.description}, genre: {movie.genre}"


@app2.put("/movies/{movie_id}")
async def update_item(movie_id: int, movie_upd: Movies):
    logger.info(f'Отработал PUT запрос для movie id = {movie_id}.')
    movie = db2.query(MoviesBase).filter(
        MoviesBase.movie_id == movie_id).first()
    movie.title = movie_upd.title
    movie.description = movie_upd.description
    movie.status = movie_upd.status
    db2.commit()
    return {"movie_id": movie_id, "movie": movie_upd}


@app2.delete("/movies/{movie_id}")
async def delete_item(movie_id: int):
    logger.info(f'Отработал DELETE запрос для movie id = {movie_id}.')
    movies = db2.query(MoviesBase).filter(
        MoviesBase.movie_id == movie_id).all()
    for movie in movies:
        db2.delete(movie)
        db2.commit()
    return {"movie_id": movie_id}
