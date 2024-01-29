from pydantic import EmailStr, BaseModel, Field


# для валидации полей таблицы
class UserInSchema(BaseModel):
    """Модель пользователя без id"""
    username: str = Field(..., max_length=25, min_length=3,
                          title='Задается username пользователя', pattern=r'^[a-zA-Z0-9_-]+$')
    email: EmailStr = Field(..., title='Задается email пользователя')
    password: str = Field(..., title='Задается пароль пользователя')


class UserSchema(UserInSchema):
    """Модель пользователя с id"""
    id: int
