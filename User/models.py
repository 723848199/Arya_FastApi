from tortoise import fields
from tortoise.models import Model


# from tortoise.contrib.pydantic import pydantic_model_creator

class UserGroup(Model):
    group_name = fields.CharField(max_length=50, description='用户组名称')
    # user = fields.ManyToManyField(model_name='models.Users')


class Users(Model):
    table = "users"
    account = fields.CharField(max_length=50, index=True, unique=True, description='账号')
    user_name = fields.CharField(max_length=50, description='用户名')
    password = fields.CharField(max_length=50, index=True, description='密码')
    phone = fields.CharField(max_length=11, index=True, null=True, unique=True, description='手机号')
    email = fields.CharField(max_length=30, index=True, null=True, unique=True, description='邮箱')
    sex = fields.CharField(max_length=10, null=True, description='性别')

    # group: fields.ForeignKeyRelation[UserGroup] = fields.ForeignKeyField(model_name='UserGroup', related_name='group')
    is_admin = fields.BooleanField(default=False, description='是否是超级管理员')
    is_delete = fields.BooleanField(default=False, description='是否删除')
    created_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    update_time = fields.DatetimeField(auto_now=True, description='最后需改时间')

    # def __str__(self):
    #     return self.user_name
    #
    # class Meta:
    #     app = ''


#
# In_User = pydantic_model_creator(Users, exclude=('id', 'is_delete', 'update_time', 'created_time'),
#                                  name='users')
# Out_User = pydantic_model_creator(Users, exclude=('password', 'is_delete'))

class Token(Model):
    pass


class UserState(Model):
    pass
