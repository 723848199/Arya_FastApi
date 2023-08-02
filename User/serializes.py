from pydantic import BaseModel, EmailStr, Field
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from User.enums import LoginTypeEnum
from User.models import Users, UserStatus


class Login(BaseModel):
    """
    用户登录模型
    """
    login_type: LoginTypeEnum = LoginTypeEnum.username
    username: str = None
    password: str = None
    phone: str = None
    email: EmailStr = None
    code: int = None


class UserRegister(BaseModel):
    username: str = Field(min_length=4, max_length=20)
    password: str = Field(min_length=4, max_items=20)


User = pydantic_model_creator(Users, )


UserIn = pydantic_model_creator(Users, exclude_readonly=True, include=('UserStatus',))
UserSchema = pydantic_model_creator(Users)


# class UserIn(BaseModel):
#     username: str
#     sex: UserSex
#
#     class Config:
#         from_attributes = True

class UserStatusSchema(pydantic_model_creator(UserStatus, include=('name',))):
    name: str
    pass


# class UserSchema(pydantic_model_creator(Users)):
#     status: UserStatusSchema = None

