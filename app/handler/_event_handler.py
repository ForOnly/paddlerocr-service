# @description: 
# @author: licanglong
# @date: 2025/11/20 14:00
from app.core import Event


class ApplicationStartupEvent(Event):
    """
    注册解析器事件
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
