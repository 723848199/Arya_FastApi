from fastapi import FastAPI
from app.user.api import login, user


def user_router(app: FastAPI):
    app.include_router(login.login_router, tags=['登录'])
    app.include_router(user.user_router, prefix='/user', tags=['用户'])
    # app.include_router(admin.admin_router, prefix='/admin', tags=['管理员'])
