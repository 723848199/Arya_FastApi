from urllib.request import Request
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


# 自定义异常返回
class HTTPException(Exception):
    def __init__(self, code: int = 400, msg: str = '请求发生错误,请核对'):
        self.msg = msg
        self.code = code


def register_exception(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def _register_exception(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.code,
            content={
                "msg": exc.msg,
            }, )


# 拦截参数校验异常
def request_validation_error(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def _request_validation_error(request: Request, exc: RequestValidationError):
        data = exc.errors()
        print(data)
        msg_list = []
        for details in data:
            par_type = details['loc'][0]
            par_name = details['loc'][1]
            print(details['msg'])
            match details['type']:
                case 'missing':
                    msg_list.append(f'{par_type} 中 {par_name} 参数不能为空')
                case '-':
                    msg_list.append('未知错误,代核对')
        return JSONResponse(
            status_code=422,
            content=msg_list
        )
