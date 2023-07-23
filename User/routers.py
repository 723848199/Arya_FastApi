from enum import Enum
from fastapi import status, APIRouter, Path
from pydantic import BaseModel
from User.models import Users

login_router = APIRouter(tags=['用户'])

user_router = APIRouter(
    prefix='/users',
    tags=['用户'],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


class UserIn(BaseModel):
    name: str
    account: str


@login_router.post('/login')
async def login(item: UserIn):
    return item


@user_router.get('/me', description='获取个人信息')
async def user_get():
    return ''


class ModelSex(str, Enum):
    man = "男"
    woman = "女"
    secrecy = "保密"


@user_router.get('/{user_id}', description='获取指定用户信息',
                 status_code=status.HTTP_200_OK)
async def user_get(user_id: int = Path(default=..., description='用户id'),
                   sex: ModelSex = Path(), ):
    print(sex)
    print(sex.value, sex.name)
    user = await Users.filter(id=user_id).first()
    if user:
        print(user.user_name)
    # raise HTTPException()
    return user


login_router.include_router(user_router)
