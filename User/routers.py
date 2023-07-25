from enum import Enum
from fastapi import status, APIRouter, Path, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from User.auth import verify_password, get_password_hash
from User.models import Users


user_router = APIRouter(
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


class UserIn(BaseModel):
    name: str
    account: str


@user_router.get('/me', summary='获取个人信息')
async def user_get():
    return ''


class ModelSex(str, Enum):
    man = "男"
    woman = "女"
    secrecy = "保密"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@user_router.get('/{user_id}', summary='获取指定用户信息',
                 status_code=status.HTTP_200_OK, )
async def user_get(user_id: int = Path(default=..., description='用户id', ),
                   token: str = Depends(oauth2_scheme)
                   ):
    print(token)
    user = await Users.filter(id=user_id).first()
    if user:
        print(user.account)
    return user


@user_router.post('/login', summary='用户登录')
async def login(username: str, password: str):
    user = await Users.filter(account=username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


@user_router.post('', summary='添加用户信息')
async def user_add(account: str, password: str):
    await Users.create(account=account, password=get_password_hash(password))
    return '添加成功'
