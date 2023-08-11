import os
from functools import cache
import dotenv
from fastapi import FastAPI
from passlib.context import CryptContext
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

# JWT令牌随机密钥,用于对jwt令牌进行签名  生成方式 openssl rand -hex 32
SECRET_KEY = "b8377f770ab26b2bc23780e82909324d0376e60953625ba99933dac7f4bfd66a"
# JWT 令牌签名算法的变量
ALGORITHM = "HS256"
# 令牌过期时间(单位:分钟)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 创建对象,进行哈希和校验密码
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@cache
class Setting:

    def __init__(self):
        self.title = 'Arya_api'
        self.summary = 'api接口完善'
        # 读取.env文件数据
        dotenv.load_dotenv()

    @property
    def db_rom_config(self):
        return {
            "connections": {
                "pgsql": {
                    'engine': 'tortoise.backends.asyncpg',
                    "credentials": {
                        'host': os.getenv('BASE_HOST', '127.0.0.1'),
                        'user': os.getenv('BASE_USER', 'arya'),
                        'password': os.getenv('BASE_PASSWORD', '12345678'),
                        'port': os.getenv('BASE_PORT', 5432),
                        'database': os.getenv('BASE_DB', 'postgres'),
                    }
                },
            },
            "apps": {
                "User": {"models": ["app.user.models"], "default_connection": "pgsql"},
                # "db2": {"models": ["models.db2"], "default_connection": "db2"},
                # "db3": {"models": ["models.db3"], "default_connection": "db3"}
            },
            'use_tz': False,
            'timezone': 'Asia/Shanghai',
            "generate_schemas": True
        }


setting = Setting()


def link_db(app: FastAPI):
    register_tortoise(
        app,
        config=setting.db_rom_config,
        generate_schemas=True,
        add_exception_handlers=False, )
