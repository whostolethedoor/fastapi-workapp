from pydantic import BaseModel, EmailStr, validator, constr
from typing import Optional
import datetime

class User(BaseModel):
    id: Optional[str] = None
    name:  str
    email: EmailStr
    hashed_passowrd: str
    is_company: bool
    created_date: datetime.datetime
    updated_date: datetime.datetime

class UserIn(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)
    password2: str
    is_company: bool = False

    @validator("password2")
    def password_confirm(cls, v, values, **kwargs):
        if 'password' in values and v != values['passowrd']:
            raise ValueError('Passwrd dnont much')
        return v