# @description: 
# @author: licanglong
# @date: 2025/11/20 14:49
from dataclasses import dataclass

from app.core import SYS_SERVER_FAIL, SYS_SERVER_SUCCESS
from app.utils.typeutils import T


@dataclass
class SysResult:
    code: int
    msg: str
    data: T

    def __init__(self, code=None, msg=None, data=None):
        self.code = code
        self.msg = msg
        self.data = data

    @staticmethod
    def fail(code=None, msg=None, data=None):
        if code is None:
            code = SYS_SERVER_FAIL
        return SysResult(code=code, msg=msg, data=data)

    @staticmethod
    def success(code=None, msg=None, data=None):
        if code is None:
            code = SYS_SERVER_SUCCESS
        return SysResult(code=code, msg=msg, data=data)

    def __str__(self):
        return f"code:{self.code},msg:{self.msg},data:{self.data}"
