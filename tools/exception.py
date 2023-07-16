from urllib.request import Request
from fastapi import FastAPI
from fastapi.responses import JSONResponse


class HTTPException(Exception):
    def __init__(self, code: int = 400, msg: str = '', data: any = None):
        self.msg = msg
        self.code = code
        self.data = data


def register_exception(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def unicorn_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=200,
            content={
                "code": exc.code,
                "msg": exc.msg,
                'data': exc.data
            }, )
