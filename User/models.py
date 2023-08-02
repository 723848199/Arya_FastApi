from tortoise import fields
from tortoise.models import Model


# from User.enums import UserType #, UserStatus, UserSex


# class UserGroup(Model):
#     group_name = fields.CharField(max_length=50, description='用户组名称')
# user = fields.ManyToManyField(model_name='models.Users')


class Users(Model):
    table = "Users"
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, index=True, unique=True, description='用户名')
    nickname = fields.CharField(max_length=50, description='昵称', null=True, default=None)
    password = fields.CharField(max_length=100, index=True, description='密码')
    phone = fields.CharField(max_length=11, null=True, unique=True, description='手机号', default=None)
    email = fields.CharField(max_length=30, null=True, unique=True, description='邮箱', default=None)
    # sex = fields.CharEnumField(enum_type=UserSex, default=UserSex.secrecy.value, max_length=10, description='性别')
    # type = fields.CharEnumField(enum_type=UserType, default=UserType.user, description='用户类型', max_length=20)
    # status = fields.CharEnumField(enum_type=UserStatus, default=UserStatus.normal.value, description='用户状态',
    #                               max_length=20)

    is_delete = fields.BooleanField(default=False, description='是否删除')
    created_time = fields.DatetimeField(auto_now_add=True, description='创建时间', null=True, default=None)
    update_time = fields.DatetimeField(auto_now=True, description='最后需改时间', null=True, default=None)
    status = fields.ForeignKeyField('User.UserStatus', related_name='user_status', null=True)
    tokens: fields.ReverseRelation['Token']

    def __str__(self):
        return self.username

    class Meta:
        app = ''

    class PydanticMeta:
        exclude = ['password']
        # include = ['User_Status']


class UserStatus(Model):
    name = fields.CharField(max_length=50)
    user_status: fields.ReverseRelation['Users']


class Token(Model):
    user: fields.ForeignKeyNullableRelation[Users] = fields.ForeignKeyField('User.Users', related_name='tokens',
                                                                            null=True)
    token = fields.CharField(max_length=255)
