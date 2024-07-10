from pydantic import BaseModel, Field, field_validator
import re


class UserRegistration(BaseModel):
    email: str = Field(..., description="Адрес электронной почты")
    password: str = Field(..., description="Пароль")

    @field_validator('email')
    def check_email(cls, value):
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, value):
            raise ValueError("Неверный формат адреса электронной почты")
        return value

    @field_validator('password')
    def check_password(cls, value):
        value = str(value)
        if len(value) < 8:
            raise ValueError("Пароль должен содержать как минимум 8 символов")
        if not any(c.isupper() for c in value):
            raise ValueError("Пароль должен содержать как минимум одну заглавную букву")
        if not any(c.islower() for c in value):
            raise ValueError("Пароль должен содержать как минимум одну строчную букву")
        if not any(c.isdigit() for c in value):
            raise ValueError("Пароль должен содержать как минимум одну цифру")
        return value