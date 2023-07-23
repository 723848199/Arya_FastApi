import os
import dotenv
from tortoise.contrib.fastapi import register_tortoise

# 读取.env文件数据
dotenv.load_dotenv()

# 数据库设置
DB_ORM_CONFIG = {
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
        "my_app": {"models": ["User.models"], "default_connection": "pgsql"},
        # "db2": {"models": ["models.db2"], "default_connection": "db2"},
        # "db3": {"models": ["models.db3"], "default_connection": "db3"}
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai',
    "generate_schemas": True
}


def link_db(app):
    register_tortoise(
        app,
        config=DB_ORM_CONFIG,
        generate_schemas=True,
        add_exception_handlers=False,
    )
