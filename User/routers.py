from fastapi import FastAPI
from User import admin, user, login


def user_routers(app: FastAPI):
    app.include_router(login.login_router, prefix='/login', tags=['登录'])
    app.include_router(user.user_router, prefix='/user', tags=['用户'])
    app.include_router(admin.admin_router, prefix='/admin', tags=['管理员'])
