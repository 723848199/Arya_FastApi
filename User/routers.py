from datetime import timedelta
from enum import Enum

from fastapi import status, APIRouter, Path, Depends, Response
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from User.auth import get_password_hash, check_user, create_access_token, check_jwt_token
from User.models import Users, Token
from settings import ACCESS_TOKEN_EXPIRE_MINUTES
from tools.exception import HTTPException

user_router = APIRouter(
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


class UserIn(BaseModel):
    name: str
    account: str


@user_router.get('/me', summary='获取个人信息')
async def user_get(user=Depends(check_jwt_token)):
    return user


class ModelSex(str, Enum):
    man = "男"
    woman = "女"
    secrecy = "保密"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@user_router.get('/{user_id}', summary='获取指定用户信息',
                 status_code=status.HTTP_200_OK, )
async def user_get(user_id: int = Path(default=..., description='用户id', )):  #
    user = await Users.filter(id=user_id).first()
    if user:
        print(user.account)
    return user


@user_router.post('/login', summary='用户登录')
async def login(username: str, password: str, response: Response):
    user = await check_user(username, password)
    if not user:
        raise HTTPException(code=status.HTTP_401_UNAUTHORIZED, msg='用户名或密码错误')

    # 创建token
    access_token = create_access_token(data={'sub': user.account})
    await Token.update_or_create(defaults={'token': access_token}, user=user)
    # 将token写入到浏览器cookie中
    response.set_cookie(key='token', value=access_token)
    return access_token


@user_router.post('', summary='添加用户信息')
async def user_add(account: str, password: str):
    await Users.create(account=account, password=get_password_hash(password))
    return '添加成功'
