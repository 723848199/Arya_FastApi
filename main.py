import uvicorn
from fastapi import FastAPI
import User.routers
from settings import DB_ORM_CONFIG
from tortoise.contrib.fastapi import register_tortoise
from tools.exception import FastAPIException

# 创建app对象
app = FastAPI()

# 挂接子路由
app.include_router(User.routers.login_router)

# 异常拦截
FastAPIException().init_app(app=app)


# 链接数据库
register_tortoise(
    app,
    config=DB_ORM_CONFIG,
    generate_schemas=True,
    add_exception_handlers=False,
)

if __name__ == '__main__':
    uvicorn.run(app='main:app', host='127.0.0.1', port=8080, reload=True)
