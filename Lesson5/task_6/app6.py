# Задание №6
# - Создать веб-страницу для отображения списка пользователей. Приложение
#   должно использовать шаблонизатор Jinja для динамического формирования HTML
#   страницы.
# - Создайте модуль приложения и настройте сервер и маршрутизацию.
# - Создайте класс User с полями id, name, email и password.
# - Создайте список users для хранения пользователей.
# - Создайте HTML шаблон для отображения списка пользователей. Шаблон должен
#   содержать заголовок страницы, таблицу со списком пользователей и кнопку для
#   добавления нового пользователя.
# - Создайте маршрут для отображения списка пользователей (метод GET).
# - Реализуйте вывод списка пользователей через шаблонизатор Jinja.


from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import logging
from fastapi import FastAPI, Request, Form
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from werkzeug.security import generate_password_hash

from Lesson5.task_6.models import Users, UsersBase, Base, engine, db6

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app6 = FastAPI()
templates = Jinja2Templates(directory="task_6/templates/")
app6.mount("/static", StaticFiles(directory="task_6/static"), name="static")


@app6.get("/users/", response_class=HTMLResponse)
async def read_root(request: Request):
    logger.info('Отработал GET запрос.')
    users = db6.query(UsersBase).all()
    return templates.TemplateResponse('index.html',
                                      {"request": request, "users": users})


@app6.get("/postdata/")
async def root_redirect():
    logger.info('Отработал GET запрос.')
    return RedirectResponse("/task_6/users/")


@app6.get("/users/{user_id}")
async def read_root(user_id: int):
    logger.info('Отработал GET запрос.')
    user = db6.query(UsersBase).filter(UsersBase.user_id == user_id).first()
    return f"User: user_id: {user.user_id}, " \
        f"name: {user.name}, email: {user.email}  "


@app6.post("/users/{user_id}")
async def create_item(user_id: int, user: Users):
    logger.info('Отработал POST запрос.')
    users = db6.query(UsersBase).filter(UsersBase.user_id == user_id).all()
    for user in users:
        if user.user_id == user_id:
            return f'Movie already exist!'
    else:
        password_hash = generate_password_hash(str(user.password))
        user = UsersBase(user_id=user_id, name=user.name,
                         email=user.email, password=password_hash, is_del=False)
        db6.add(user)
        db6.commit()
        return f"User: user_id: {user.user_id}, " \
            f"name: {user.name}, email: {user.email}  "


@app6.post("/users/")
async def create_user(user: Users):
    user_id = 1
    logger.info('Отработал POST запрос.')
    users = db6.query(UsersBase).all()
    if db6.query(UsersBase.user_id).first():
        for usr in users:
            if user_id == usr.user_id:
                user_id += 1
            else:
                break
        password_hash = generate_password_hash(str(user.password))
        new_user = UsersBase(user_id=user_id, name=user.name,
                             email=user.email, password=password_hash, is_del=False)
        db6.add(new_user)
        db6.commit()
        return f"User: user_id: {new_user.user_id}, " \
            f"name: {new_user.name}, email: {new_user.email}  "

    else:
        password_hash = generate_password_hash(str(user.password))
        new_user = UsersBase(user_id=user_id, name=user.name,
                             email=user.email, password=password_hash, is_del=False)
        db6.add(new_user)
        db6.commit()
        return f"User: user_id: {new_user.user_id}, " \
            f"name: {new_user.name}, email: {new_user.email}  "


@app6.post("/postdata/", response_class=HTMLResponse)
def postdata(request: Request, name=Form(), email=Form(), password=Form()):
    user_id = 1
    logger.info('Отработал POST запрос.')
    users = db6.query(UsersBase).all()
    if db6.query(UsersBase.user_id).first():
        for user in users:
            if user_id == user.user_id:
                user_id += 1
            else:
                break
        password_hash = generate_password_hash(str(password))
        new_user = UsersBase(user_id=user_id, name=name,
                             email=email, password=password_hash, is_del=False)
        db6.add(new_user)
        db6.commit()
        return templates.TemplateResponse('index.html',
                                          {"request": request, "users": users})

    else:
        password_hash = generate_password_hash(str(password))
        new_user = UsersBase(user_id=user_id, name=name,
                             email=email, password=password_hash, is_del=False)
        db6.add(new_user)
        db6.commit()
        return templates.TemplateResponse('index.html',
                                          {"request": request, "users": users})


@app6.put("/users/{user_id}")
async def update_item(user_id: int, user_upd: Users):
    logger.info(f'Отработал PUT запрос для movie id = {user_id}.')
    user = db6.query(UsersBase).filter(UsersBase.user_id == user_id).first()
    user.name = user_upd.name
    user.email = user_upd.email
    user.password = user_upd.password
    db6.commit()
    return {"user_id": user_id, "user": user_upd}


@app6.delete("/users/{user_id}")
async def delete_item(user_id: int):
    logger.info(f'Отработал DELETE запрос для movie id = {user_id}.')
    users = db6.query(UsersBase).filter(UsersBase.user_id == user_id).all()
    for user in users:
        db6.delete(user)
        db6.commit()
    return {"user_id": user_id}
