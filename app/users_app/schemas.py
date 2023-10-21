from pydantic import BaseModel, EmailStr, validator

from app.users_app.utils import validate_password_strength


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    email: EmailStr

    @validator("password")
    def validate_password_strength(cls, value):
        print(value,len(value))
        if not validate_password_strength(value):
            raise ValueError("Password does not meet the criteria")
        return value


class User(UserBase):
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
