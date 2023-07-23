from fastapi import APIRouter

from User.routers import login_router

main_router = APIRouter(
    responses={404: {"description": "Not found"}},
)

main_router.include_router(login_router)
