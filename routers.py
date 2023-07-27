from fastapi import FastAPI

from User.routers import user_routers


def main_router(app: FastAPI):
    """
    路由管理
    """
    user_routers(app=app)
