from typing import List
from fastapi import Depends, status, Path, Response, APIRouter
from User.auth import check_jwt_token
from User.models import Users
from User.serializes import UserOut
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


@user_router.get('/me', summary='获取个人信息', response_model=UserOut)
async def user_get(user=Depends(check_jwt_token)):
    return user


@user_router.get('/all', summary='获取所有用户信息', response_model=List[UserOut])
async def user_all():
    users = await Users.all()
    if not users:
        raise HTTPException(msg='请求的数据不存在')
    return users


@user_router.get('/{user_id}', summary='获取指定用户信息',
                 status_code=status.HTTP_200_OK, response_model=UserOut)
async def user_get(user_id: int = Path(default=..., description='用户id', )):
    user = await Users.filter(id=user_id).first()
    if not user:
        raise HTTPException(msg='请求的数据不存在')
    return user
