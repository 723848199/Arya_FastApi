from fastapi import APIRouter, Depends
from User.auth import check_admin_token

# 超级管理员路由--仅管理员可以访问
admin_router = APIRouter(
    dependencies=[Depends(check_admin_token)],
    responses={404: {"description": "Not found"}},
)


@admin_router.get('/')
async def demo():
    return '---'
