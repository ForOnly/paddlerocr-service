# @description: 
# @author: licanglong
# @date: 2025/11/20 15:32
import logging
import os

from app.client.PaddleOcrClient import PaddleOcrPool
from app.configure.ModelConfigure import ModelsEnum
from app.core import EventBusInstance
from app.handler import ApplicationStartupEvent

_EM = EventBusInstance()
_log = logging.getLogger(__name__)


@_EM.subscribe(ApplicationStartupEvent)
def init_logger_onstartup(event: ApplicationStartupEvent):
    # PaddleOcrPool(ModelsEnum.PP_OCRV4_MOBILE, pool_size=os.cpu_count())
    PaddleOcrPool(ModelsEnum.PP_OCRV5_MOBILE, pool_size=os.cpu_count())
    # PaddleOcrPool(ModelsEnum.PP_OCRV5_SERVER, pool_size=os.cpu_count())
