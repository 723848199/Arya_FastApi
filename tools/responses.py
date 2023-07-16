import fastapi.openapi.utils
import starlette.status


def responses(code: int = starlette.status.HTTP_200_OK, msg: str = '操作成功', data: any = None):
    return {'code': code, 'msg': msg, 'data': data}
