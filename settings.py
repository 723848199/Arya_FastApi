import os
import dotenv

# 读取.env文件数据
dotenv.load_dotenv()

# 数据库设置

DB_ORM_CONFIG = {
    "connections": {
        "base": {
            'engine': 'tortoise.backends.mysql',
            "credentials": {
                'host': os.getenv('BASE_HOST', '127.0.0.1'),
                'user': os.getenv('BASE_USER', 'root'),
                'password': os.getenv('BASE_PASSWORD', '123456'),
                'port': int(os.getenv('BASE_PORT', 3306)),
                'database': os.getenv('BASE_DB', 'base'),
            }
        },
    },
    "apps": {
        "base": {"models": ["models.base"], "default_connection": "base"},
        # "db2": {"models": ["models.db2"], "default_connection": "db2"},
        # "db3": {"models": ["models.db3"], "default_connection": "db3"}
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}

print(DB_ORM_CONFIG['connections']['base'])
# async def register_mysql(app: FastAPI):
#     # 注册数据库
#     register_tortoise(
#         app,
#         config=DB_ORM_CONFIG,
#         generate_schemas=False,
#         add_exception_handlers=False,
#     )
