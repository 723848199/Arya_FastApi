from fastapi import status, APIRouter, Form, Body, Response
from User.auth import check_user, create_access_token, get_password_hash
from User.enums import LoginTypeEnum
from User.models import Token, Users
from User.serializes import User, UserIn, Login, UserRegister, UserSchema
from tools.exception import HTTPException

# 登录路由--不需要验证token
login_router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@login_router.post('/login', summary='用户登录', response_model='')
async def login(user: Login, response: Response):
    if user.login_type == LoginTypeEnum.username:
        user = await check_user(user.username, user.password)
        if not user:
            raise HTTPException(code=status.HTTP_401_UNAUTHORIZED, msg='用户名或密码错误')
        # 创建token
        access_token = create_access_token(data={'sub': user.username})
        await Token.update_or_create(defaults={'token': access_token}, user=user)
        # 将token写入到浏览器cookie中
        response.set_cookie(key='token', value=access_token)
        return access_token


@login_router.post('/register', summary='注册用户', response_model=UserSchema)
async def register(user: UserRegister = Body()):
    # user.password = get_password_hash(user.password)
    # if await Users.get_or_none(username=user.username):
    #     raise HTTPException(msg='账户已存在')
    # user_obj = await Users.create(**user.model_dump())
    user_obj = await Users.filter(username=user.username).first()
    # p =  await UserIn.from_tortoise_orm(user_obj)
    # p.model_dump_json(indent=4)
    # return  p
    print(user_obj)
    return await UserSchema.from_tortoise_orm(user_obj)
