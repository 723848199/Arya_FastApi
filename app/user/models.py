from typing import Optional, Iterable
from tortoise import fields, Model, BaseDBAsyncClient
from app.models import Abstract
from setting import pwd_context


class User(Abstract):
    account = fields.CharField(max_length=50, index=True, unique=True, description='账号', null=True)
    username = fields.CharField(max_length=50, description='用户名', null=True, default=None)
    password = fields.CharField(max_length=100, index=True, description='密码')

    tokens: fields.ReverseRelation['Token']

    class Meta:
        table = 'users'

    class PydanticMeta:
        exclude = ['password']


class Token(Model):
    user: fields.ForeignKeyNullableRelation[User] = fields.ForeignKeyField('User.User', related_name='tokens',
                                                                           null=True)
    token = fields.CharField(max_length=255)


from enum import IntEnum


class Gender(IntEnum):
    man = 1
    woman = 2
    secrecy = 0


class UserModel(Abstract):
    """
    ipynb测试模型
    """
    account = fields.CharField(max_length=50, index=True, description='账号', null=True)
    password = fields.CharField(max_length=100, index=True, description='密码')
    gender = fields.IntEnumField(enum_type=Gender, defalut=Gender.secrecy.value, )
    integral = fields.DecimalField(max_digits=10, decimal_places=5, null=True, default=None)
