from fastapi import status, APIRouter, Form, Body, Response
from User.auth import check_user, create_access_token, get_password_hash
from User.models import Token, Users, UserType
from User.serializes import UserIn, UserOut
from tools.exception import HTTPException

# 登录路由--不需要验证token
login_router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@login_router.post('/login', summary='用户登录', response_model='')
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


@login_router.post('/register', summary='注册用户', response_model=UserOut)
async def register(user: UserIn = Body()):
    user.password = get_password_hash(user.password)
    if await Users.filter(account=user.account).first():
        raise HTTPException(msg='账户已存在')
    user = await Users.create(**user.model_dump())
    return user
