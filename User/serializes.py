from pydantic import BaseModel, EmailStr, Field

from User.enums import UserSex


class UserOut(BaseModel):
    account: str = Field(min_length=4, max_length=20)
    username: str
    # email: EmailStr = None
    # phone: str = Field(default=None, max_length=11)
    sex: UserSex = Field(default=UserSex.secrecy)


class UserIn(UserOut):
    password: str
