from enum import Enum


class UserType(Enum):
    """
    用户类型
    """
    user = '普通用户'
    admin = '管理员用户'


class UserStatus(Enum):
    """
    用户状态
    """
    normal = '正常'
    delete = '已删除'


class UserSex(Enum):
    """
    用户性别
    """
    man: str = '男'
    woman: str = '女'
    secrecy: str = '保密'


class LoginTypeEnum(Enum):
    """
    登录类型
    1,账号密码登录
    2,手机号登录
    3,邮箱登录
    """
    username: int = 1
    mobile_phone: int = 2
    email: int = 3
