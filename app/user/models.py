from typing import Optional, Iterable
from tortoise import fields, Model, BaseDBAsyncClient
from app.models import Abstract
from setting import pwd_context


class User(Abstract):
    account = fields.CharField(max_length=50, index=True, unique=True, description='账号', null=True)
    username = fields.CharField(max_length=50, description='用户名', null=True, default=None)
    password = fields.CharField(max_length=100, index=True, description='密码')

    tokens: fields.ReverseRelation['Token']

    async def save(
            self,
            using_db: Optional[BaseDBAsyncClient] = None,
            update_fields: Optional[Iterable[str]] = None,
            force_create: bool = False,
            force_update: bool = False,
    ) -> None:
        """
        重写save方法,保存时对密码进行加密
        """
        if force_create or 'password' in update_fields:
            self.password = pwd_context.hash(self.password)
        await super(User, self).save(using_db, update_fields, force_create, force_update)

    class Meta:
        table = 'users'

    class PydanticMeta:
        exclude = ['password']


class Token(Model):
    user: fields.ForeignKeyNullableRelation[User] = fields.ForeignKeyField('User.User', related_name='tokens',
                                                                           null=True)
    token = fields.CharField(max_length=255)
