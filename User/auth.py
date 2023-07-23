from fastapi import Header
from starlette import status

from tools.exception import HTTPException


async def get_token_header(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(code=status.HTTP_401_UNAUTHORIZED, msg='token校验失败')
    return 'arya'
