from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from app.user.models import User


class Login(BaseModel):
    account: str
    password: str
    username: str = None

    class Config:
        from_attributes = True


UserOut = pydantic_model_creator(User)
