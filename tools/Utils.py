import hashlib
import uuid
from random import randrange


def code_number(length: int):
    """
    随机数字
    :param length: 长度
    :return: str
    """
    code = ""
    for i in range(length):
        ch = chr(randrange(ord('0'), ord('9') + 1))
        code += ch

    return code


def random_str():
    """
    唯一随机字符串
    :return: str
    """
    only = hashlib.md5(str(uuid.uuid1()).encode(encoding='UTF-8')).hexdigest()
    print(uuid.uuid1())
    return only


#
# def en_password(psw: str):
#     """
#     密码加密
#     :param psw: 需要加密的密码
#     :return: 加密后的密码
#     """
#     password = pbkdf2_sha256.hash(psw)
#     return password
#
#
# def check_password(password: str, old: str):
#     """
#     密码校验
#     :param password: 用户输入的密码
#     :param old: 数据库密码
#     :return: Boolean
#     """
#     check = pbkdf2_sha256.verify(password, old)
#     if check:
#         return True
#     else:
#         return False



