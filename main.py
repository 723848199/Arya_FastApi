import uvicorn
from fastapi import FastAPI
import User.routers
from tools.exception import register_exception

# 创建app对象
app = FastAPI()

# 挂接子路由
app.include_router(User.routers.login_router)

# 异常拦截
register_exception(app)

if __name__ == '__main__':
    uvicorn.run(app='main:app', host='127.0.0.1', port=8000, reload=True)
