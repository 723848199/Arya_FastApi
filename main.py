import uvicorn
from fastapi import FastAPI
from app.routers import main_router
from common.exception import FastAPIException
from setting import link_db, setting

app = FastAPI(
    title=setting.title,
    summary=setting.summary
)

# 挂接子路由
main_router(app=app)

# 异常拦截
FastAPIException(app)

# 链接数据库
link_db(app=app)

# 运行app
if __name__ == '__main__':
    uvicorn.run(app='main:app', host='127.0.0.1', port=8080, reload=True)
