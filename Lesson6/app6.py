# Необходимо создать базу данных для интернет-магазина. База данных должна состоять из трех таблиц: товары, заказы и
# пользователи.
# Таблица товары должна содержать информацию о доступных товарах, их описаниях и ценах.
# Таблица пользователи должна содержать информацию о зарегистрированных пользователях магазина.
# Таблица заказы должна содержать информацию о заказах, сделанных пользователями.
# - Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY),
#   имя, фамилия, адрес электронной почты и пароль.
# - Таблица товаров должна содержать следующие поля: id (PRIMARY KEY),
#   название, описание и цена.
# - Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id
#   пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус
#   заказа.
# Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц
# (итого шесть моделей).
# Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API (итого 15 маршрутов).
# - Чтение всех
# - Чтение одного
# - Запись
# - Изменение
# - Удаление


from typing import List
from datetime import datetime
import random
from passlib.context import CryptContext
from models import UserModel, OrderModel, ProductModel
from schemas import UserInSchema, UserSchema, ProductSchema, OrderSchema
from fastapi import FastAPI, HTTPException
from database import startup, shutdown, db
from sqlalchemy import select, delete, insert, update
from tools import get_password_hash


app6 = FastAPI(title='Shop')
app6.add_event_handler("startup", startup)
app6.add_event_handler("shutdown", shutdown)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------- READ ALL ----------

@app6.get("/users/", response_model=List[UserSchema])
async def get_all_users() -> List[UserSchema]:
    """Получение списка всех пользователей: GET /users/"""
    query = select(UserModel)
    users = await db.fetch_all(query)
    if users:
        return users
    raise HTTPException(status_code=404, detail="Нет ни одного пользователя")


@app6.get("/products/", response_model=List[ProductSchema])
async def get_all_products() -> List[ProductSchema]:
    """Получение списка всех продуктов: GET /products/"""
    query = select(ProductModel)
    products = await db.fetch_all(query)
    if products:
        return products
    raise HTTPException(status_code=404, detail="Нет ни одного продукта")


@app6.get("/orders/", response_model=List[OrderSchema])
async def get_all_orders() -> List[OrderSchema]:
    """Получение списка всех заказов: GET /orders/"""
    query = select(OrderModel)
    orders = await db.fetch_all(query)
    if orders:
        return orders
    raise HTTPException(status_code=404, detail="Нет ни одного заказа")


# ---------- READ ONE ----------

@app6.get('/users/{user_id}', response_model=UserSchema)
async def get_single_user(user_id: int) -> UserSchema:
    """Получение информации о конкретном пользователе: GET /users/{user_id}/"""
    query = select(UserModel).where(UserModel.id == user_id)
    db_user = await db.fetch_one(query)
    if db_user:
        return db_user
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@app6.get('/products/{product_id}', response_model=ProductSchema)
async def get_single_product(product_id: int) -> ProductSchema:
    """Получение информации о конкретном продукте: GET /products/{product_id}/"""
    query = select(ProductModel).where(ProductModel.id == product_id)
    db_product = await db.fetch_one(query)
    if db_product:
        return db_product
    raise HTTPException(status_code=404, detail="Продукт не найден")


@app6.get("/orders/{order_id}", response_model=OrderSchema)
async def get_single_order(order_id: int) -> OrderSchema:
    """Получение информации о конкретном заказе: GET /orders/{order_id}/"""
    query = select(OrderModel).where(OrderModel.id == order_id)
    order = await db.fetch_one(query)
    if order:
        return order
    raise HTTPException(status_code=404, detail="Заказ не найден")


# ---------- CREATE ----------

@app6.post('/users/', response_model=UserSchema)
async def create_user(user: UserInSchema) -> dict:
    """Создание нового пользователя: POST /users/"""
    hashed_password = await get_password_hash(user.password)
    user_dict = user.model_dump()
    user_dict['password'] = hashed_password
    query = insert(UserModel).values(**user_dict)
    user_id = await db.execute(query, user_dict)
    return {**user_dict, 'id': user_id}


@app6.post('/products/', response_model=ProductSchema)
async def create_product(product: ProductSchema) -> dict:
    """Создание нового продукта: POST /products/"""
    product_dict = product.model_dump()
    query = insert(ProductModel).values(**product_dict)
    product_id = await db.execute(query)
    return {**product_dict, 'id': product_id}


@app6.post("/orders/", response_model=OrderSchema)
async def create_order(order: OrderSchema) -> dict:
    """Создание нового заказа: POST /orders/"""
    order_dict = order.model_dump()
    query = insert(OrderModel).values(**order_dict)
    order_id = await db.execute(query)
    return {**order_dict, 'id': order_id}


# ---------- UPDATE ----------

@app6.put('/users/{user_id}', response_model=UserSchema)
async def update_user(user_id: int, user: UserInSchema) -> UserSchema:
    """Обновление информации о пользователе: PUT /users/{user_id}/"""
    query = select(UserModel).where(UserModel.id == user_id)
    db_user = await db.fetch_one(query)
    if db_user:
        updated_user = user.model_dump(exclude_unset=True)
        if 'password' in updated_user:
            updated_user['password'] = await get_password_hash(updated_user.pop('password'))
        query = update(UserModel).where(UserModel.id == user_id).values(updated_user)
        await db.execute(query)
        return await db.fetch_one(select(UserModel).where(UserModel.id == user_id))
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@app6.put("/products/{product_id}", response_model=ProductSchema)
async def update_product(product_id: int, product: ProductSchema) -> ProductSchema:
    """Обновление информации о продукте: PUT /products/{product_id}/"""
    query = select(ProductModel).where(ProductModel.id == product_id)
    db_product = await db.fetch_one(query)
    if db_product:
        updated_product = product.model_dump(exclude_unset=True)
        query = update(ProductModel).where(ProductModel.id == product_id).values(updated_product)
        await db.execute(query)
        return await db.fetch_one(select(ProductModel).where(ProductModel.id == product_id))
    raise HTTPException(status_code=404, detail="Продукт не найден")


@app6.put("/orders/{order_id}", response_model=OrderSchema)
async def update_order(order_id: int, order: OrderSchema) -> OrderSchema:
    """Обновление информации о заказе: PUT /orders/{order_id}/"""
    query = select(OrderModel).where(OrderModel.id == order_id)
    db_order = await db.fetch_one(query)
    if db_order:
        updated_order = order.model_dump(exclude_unset=True)
        query = update(OrderModel).where(OrderModel.id == order_id).values(updated_order)
        await db.execute(query)
        return await db.fetch_one(select(OrderModel).where(OrderModel.id == order_id))
    raise HTTPException(status_code=404, detail="Заказ не найден")


# ---------- DELETE ----------

@app6.delete("/users/{user_id}")
async def delete_user(user_id: int) -> dict:
    """Удаление пользователя: DELETE /users/{user_id}/"""
    query = select(UserModel).where(UserModel.id == user_id)
    db_user = await db.fetch_one(query)
    if db_user:
        query = delete(UserModel).where(UserModel.id == user_id)
        await db.execute(query)
        return {'detail': f'Пользователь с id={db_user.id} удален'}
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@app6.delete("/products/{product_id}")
async def delete_product(product_id: int) -> dict:
    """Удаление продукта: DELETE /products/{product_id}/"""
    query = select(ProductModel).where(ProductModel.id == product_id)
    db_product = await db.fetch_one(query)
    if db_product:
        query = delete(ProductModel).where(ProductModel.id == product_id)
        await db.execute(query)
        return {"detail": f"Продукт с id={product_id} удален"}
    raise HTTPException(status_code=404, detail="Продукт не найден")


@app6.delete("/orders/{order_id}")
async def delete_order(order_id: int) -> dict:
    """Удаление заказа: DELETE /orders/{order_id}/"""
    query = select(OrderModel).where(OrderModel.id == order_id)
    db_order = await db.fetch_one(query)
    if db_order:
        query = delete(OrderModel).where(OrderModel.id == order_id)
        await db.execute(query)
        return {"detail": f"Заказ с id={order_id} удален"}
    raise HTTPException(status_code=404, detail="Заказ не найден")


if __name__ == '__main__':
    import asyncio

    asyncio.run(startup())

    # Создание БД shop.db и наполнение таблиц тестовыми данными
    async def virgin_db():
        # Удаление существующих записей
        await db.execute(delete(UserModel))
        await db.execute(delete(ProductModel))
        await db.execute(delete(OrderModel))

        # Заполнение таблицы пользователей
        user_query = insert(UserModel)
        for i in range(1, 11):
            password = pwd_context.hash(f'password{i}')
            new_user = {"firstname": f"FirstName{i}", "lastname": f"LastName{i}", "email": f"user{i}@mail.ru",
                        "password": password}
            await db.execute(user_query, new_user)

        # Заполнение таблицы товаров
        product_query = insert(ProductModel)
        for i in range(1, 11):
            new_product = {"name": f"Product{i}", "description": f"Description of Product{i}", "price": i * 10.0}
            await db.execute(product_query, new_product)

        # Заполнение таблицы заказов
        order_query = insert(OrderModel)
        for i in range(1, 11):
            new_order = {
                "user_id": i,
                "product_id": i,
                "order_date": datetime.now(),
                "status": random.choice(["NEW", "PAID", "SENT", "DELIVERED", "CANCELLED"])
            }
            await db.execute(order_query, new_order)


    asyncio.run(virgin_db())
