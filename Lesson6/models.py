from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserModel(Base):
    """Таблица Users"""
    __tablename__ = 'users'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    firstname = Column(String(length=50), index=True)
    lastname = Column(String(length=50), index=True)
    email = Column(String(length=50), unique=True, index=True)
    password = Column(String, nullable=False)

    def __str__(self):
        return self.firstname

    def __repr__(self):
        return f'User(id={self.id}, firstname={self.firstname}, lastname={self.lastname}, email={self.email})'


class ProductModel(Base):
    """Таблица Products"""
    __tablename__ = 'products'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(length=50), unique=True, index=True)
    description = Column(Text, index=True)
    price = Column(Float, index=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Product(id={self.id}, name={self.name}, description={self.description}, price={self.price})'


class OrderModel(Base):
    """Таблица Orders"""
    __tablename__ = 'orders'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50))

    def __repr__(self):
        return f'Order(id={self.id}, user_id={self.user_id}, product_id={self.product_id})'
