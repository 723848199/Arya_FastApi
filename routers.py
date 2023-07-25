from fastapi import FastAPI
from User.routers import user_router


def main_router(app: FastAPI):
    """
    路由管理
    """
    app.include_router(user_router, prefix='/user', tags=['用户'])
