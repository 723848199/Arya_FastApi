import uvicorn
from fastapi import FastAPI
from routers import main_router
from settings import link_db
from tools.exception import FastAPIException

# 创建app对象
app = FastAPI(debug=True,
              title='FL_api',
              summary='测试用例api提供',
              description='试验,逐步完善api',
              )

# 挂接子路由
main_router(app=app)

# 异常拦截
FastAPIException(app=app)

# 链接数据库
link_db(app=app)

# 运行app
if __name__ == '__main__':
    uvicorn.run(app='main:app', host='127.0.0.1', port=8080, reload=True)
