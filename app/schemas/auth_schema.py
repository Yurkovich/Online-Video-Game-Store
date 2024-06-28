from pydantic import BaseModel, Field, field_validator
import re


class UserRegistration(BaseModel):
    email: str = Field(..., description="Адрес электронной почты")
    password: str = Field(..., description="Пароль")

    # Определение валидатора для поля email
    @field_validator('email')
    def check_email(cls, value):
        # Используем регулярное выражение для проверки формата email
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, value):
            raise ValueError("Неверный формат адреса электронной почты")
        return value

    # Определение валидатора для поля password
    @field_validator('password')
    def check_password(cls, value):
        # Преобразуем пароль в строку, если он ещё не строка
        value = str(value)
        # Проверяем, что пароль содержит как минимум 8 символов, одну заглавную букву, одну строчную букву и одну цифру
        if len(value) < 8:
            raise ValueError("Пароль должен содержать как минимум 8 символов")
        if not any(c.isupper() for c in value):
            raise ValueError("Пароль должен содержать как минимум одну заглавную букву")
        if not any(c.islower() for c in value):
            raise ValueError("Пароль должен содержать как минимум одну строчную букву")
        if not any(c.isdigit() for c in value):
            raise ValueError("Пароль должен содержать как минимум одну цифру")
        return value