from datetime import datetime, timedelta
from typing import Union, Optional

from fastapi import Header, Response, Cookie
from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from starlette import status

from User.models import Users, Token
from settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from tools.exception import HTTPException

# 创建对象,进行哈希和校验密码
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
    校验密码
    :param plain_password: 原密码
    :param hashed_password: 哈希后的密码
    :return: bool  校验成功返回True,反之False
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    哈希来自用户的密码
    :param password: 原密码
    :return: 哈希后的密码
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    """
    访问令牌,创建token
    :param data: 需要JWT令牌加密的数据
    :param expires_delta: 令牌有效期
    :return: token
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    # 添加失效时间
    to_encode.update({"exp": expire})
    # SECRET_KEY:密钥
    # ALGORITHM:令牌签名算法
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def check_jwt_token(token: str = Cookie(default=None), response: Response = None) -> Union[Users, None]:
    """
    验证token
    :param response:
    :param token:
    :return: 用户
    """
    if not token:
        raise HTTPException(code=status.HTTP_401_UNAUTHORIZED, msg='token验证失败,不能为空')
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        username: str = payload.get('sub')
        user = await Users.filter(account=username).first()
        # if datetime.utcnow() + timedelta(minutes=10) > datetime.utcfromtimestamp(payload.get('exp')):
        # 创建token
        access_token = create_access_token(data={'sub': user.account})
        response.headers['token'] = access_token
        response.set_cookie(key='token', value=access_token)
        await Token.update_or_create(defaults={'token': access_token}, user=user)
        return user
    except (jwt.JWTError, jwt.ExpiredSignatureError, ValidationError):
        raise HTTPException(code=status.HTTP_401_UNAUTHORIZED, msg='token验证失败')


async def check_user(username, password) -> Union[Users, bool]:
    """
    校验用户密码
    :param username: 账号
    :param password: 密码
    :return:
    """
    user = await Users.filter(account=username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
