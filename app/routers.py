from fastapi import FastAPI
from app.user.routers import user_router


def main_router(app: FastAPI):
    """
    路由管理
    """
    # 用户
    user_router(app=app)
