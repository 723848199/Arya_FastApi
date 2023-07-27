from fastapi.openapi.models import Response
from fastapi import status, APIRouter
from User.auth import check_user, create_access_token
from User.models import Token, Users, UserType
from tools.exception import HTTPException

# 登录路由--不需要验证token
login_router = APIRouter(
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@login_router.post('', summary='用户登录')
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


@login_router.post('/adduser', summary='添加用户')
async def login(username: str, password: str, response: Response):
    user = await Users.create(account=username, password=password, type=UserType.admin)
    return user


@login_router.post('/adduser01', summary='添加用户')
async def login(user_id: int = 1):
    user = await Users.filter(type=UserType.user).first()
    print(user.type)
    if user.type == UserType.user:
        print('----')
    return user
