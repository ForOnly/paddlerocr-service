# @description: 
# @author: licanglong
# @date: 2025/1/13 11:49
from app.core._constants import SYS_SERVER_FAIL, SYS_SERVER_FAIL_MSG


class BizException(Exception):
    """
    业务异常
    """

    def __init__(self, message: str = None, code: int = SYS_SERVER_FAIL):
        self.message = message or SYS_SERVER_FAIL_MSG
        self.code = code
