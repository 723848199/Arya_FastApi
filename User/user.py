from typing import List, Union
from fastapi import Depends, status, Path, Response, APIRouter
from User.auth import check_jwt_token
from User.models import Users
from User.serializes import UserIn
from tools.exception import HTTPException

# 用户路由--需要验证token-登录后可以访问
user_router = APIRouter(
    dependencies=[Depends(check_jwt_token)],
    responses={404: {"description": "Not found"}},
)


@user_router.delete('/logout', summary='退出登录')
async def user_logout(response: Response):
    response.delete_cookie(key='token')
    return '操作成功'


@user_router.get('/me', summary='获取个人信息', response_model=UserIn)
async def user_get(user: Users = Depends(check_jwt_token)):
    print('------')
    return user


@user_router.get('/all', summary='获取所有用户信息', response_model=List[UserIn])
async def user_all():
    users = await Users.all()
    # return await UserIn.from_queryset(users)
    return users


@user_router.get('/{user_id}', summary='获取指定用户信息',
                 status_code=status.HTTP_200_OK, response_model=Union[UserIn, None])
async def user_get(user_id: int = Path(default=..., description='用户id', )):
    user = await Users.get_or_none(id=user_id)
    if not user:
        raise HTTPException(msg='请求的数据不存在')
    return user
