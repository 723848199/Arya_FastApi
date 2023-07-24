from enum import Enum
from fastapi import status, APIRouter, Path
from pydantic import BaseModel
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


@user_router.get('/{user_id}', summary='获取指定用户信息',
                 status_code=status.HTTP_200_OK, include_in_schema=False)
async def user_get(user_id: int = Path(default=..., description='用户id'),
                   sex: ModelSex = Path(), ):
    print(sex)
    print(sex.value, sex.name)
    user = await Users.filter(id=user_id).first()
    if user:
        print(user.user_name)
    return user
