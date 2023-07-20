from fastapi import APIRouter, Depends
from fastapi import Header, status
from tools.exception import HTTPException

from tools.responses import responses


async def get_token_header(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(code=status.HTTP_401_UNAUTHORIZED, msg='token校验失败')
    return 'arya'


login_router = APIRouter()

user_router = APIRouter(
    prefix='/users',
    tags=['用户'],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},

)


@login_router.get('/login')
async def login():
    return {'msg': '登录成功'}


@user_router.get('/get/', )
async def user_get(user, ):
    return responses()


login_router.include_router(user_router)