from fastapi import Header
from passlib.context import CryptContext
from starlette import status
from tools.exception import HTTPException


async def get_token_header(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        raise HTTPException(code=status.HTTP_401_UNAUTHORIZED, msg='token校验失败')
    return 'arya'


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
    验证密码是否正确
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    # 哈希密码--密码加密
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        pass
