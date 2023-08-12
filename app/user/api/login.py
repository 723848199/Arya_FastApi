from fastapi import APIRouter, Body, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas import Login, UserOut
from app.user.auth import verify_password, create_access_token
from app.user.models import User, Token
from common.exception import HTTPException

# 登录路由--不需要验证token
login_router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@login_router.post('/register', summary='用户注册', response_model=UserOut)
async def register(user: Login = Body()):
    if await User.get_or_none(account=user.account):
        raise HTTPException(msg=f'{user.account} 用户已存在')
    user_obj = await User.create(**user.model_dump())
    return await UserOut.from_tortoise_orm(user_obj)


@login_router.post('/login', summary='用户登录', )
async def login(user_data: OAuth2PasswordRequestForm = Depends()):
    if user_obj := await User.get_or_none(account=user_data.username, is_delete=False):
        if verify_password(user_data.password, user_obj.password):
            # 创建token
            access_token = create_access_token(data={'sub': user_obj.account})
            await Token.update_or_create(defaults={'token': access_token}, user=user_obj)
            # 将token写入到浏览器cookie中
            response = Response()
            response.set_cookie(key='token', value=access_token)
            return response
        else:
            raise HTTPException(msg='用户名或密码错误')
    else:
        raise HTTPException(msg='账号不存在或已注销')
