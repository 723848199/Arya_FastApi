from typing import List, Union
from fastapi import Depends, status, Path, Response, APIRouter, Body

from app.schemas import UserOut
from app.user.auth import check_jwt_token
from app.user.models import User
from common.exception import HTTPException
from setting import pwd_context

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
async def user_get(user: User = Depends(check_jwt_token)):
    return await UserOut.from_tortoise_orm(user)


@user_router.get('/all', summary='获取所有用户信息', response_model=List[UserOut])
async def user_all():
    return await UserOut.from_queryset(User.filter(is_delete=False))


@user_router.get('/{user_id}', summary='获取指定用户信息',
                 status_code=status.HTTP_200_OK, response_model=Union[UserOut])
async def user_get(user_id: int = Path(default=..., description='用户id', )):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(msg='请求的数据不存在')
    return await UserOut.from_tortoise_orm(user)


@user_router.put('/me', summary='重置密码')
async def reset_password(user: User = Depends(check_jwt_token), new_password: str = Body()):
    new_password = pwd_context.hash(new_password)
    await User.filter(pk=user.pk).update(password=new_password)
    return '操作成功'
