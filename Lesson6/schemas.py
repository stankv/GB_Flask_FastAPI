from pydantic import EmailStr, BaseModel, Field
from datetime import datetime
from typing import Optional


class ProductSchema(BaseModel):
    """Модель продукта"""
    id: Optional[int] = Field(None, title='ID продукта')
    name: str = Field(..., max_length=50, title='Название продукта')
    description: str = Field(..., title='Описание продукта')
    price: float = Field(..., title='Цена продукта')


class OrderSchema(BaseModel):
    """Модель заказа"""
    id: Optional[int] = Field(None, title='ID заказа')
    user_id: int = Field(..., title='ID пользователя, сделавшего заказ')
    product_id: int = Field(..., title='ID заказанного продукта')
    order_date: datetime = Field(default_factory=datetime.now, title='Дата заказа')
    status: str = Field('new', max_length=50, title='Статус заказа')


class UserInSchema(BaseModel):
    """Модель пользователя без id"""
    firstname: str = Field(..., max_length=25, min_length=3,
                           title='Задается firstname пользователя', pattern=r'^[a-zA-Z0-9_-]+$')
    lastname: str = Field(..., max_length=25, min_length=3,
                          title='Задается lastname пользователя', pattern=r'^[a-zA-Z0-9_-]+$')
    email: EmailStr = Field(..., title='Задается email пользователя')
    password: str = Field(..., title='Задается пароль пользователя')


class UserSchema(UserInSchema):
    """Модель пользователя с id"""
    id: int
