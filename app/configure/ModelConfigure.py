# @description: 
# @author: licanglong
# @date: 2025/11/19 13:50
from dataclasses import dataclass
from enum import Enum, unique
from typing import Optional

from app.utils.pathutils import getpath


@dataclass
class ModelModule:
    name: Optional[str] = None
    path: Optional[str] = None


@unique
class ModelsEnum(Enum):
    det: ModelModule
    rec: ModelModule

    PP_OCRV4_MOBILE = (ModelModule("PP-OCRv4_mobile_det", getpath("models/PP-OCRv4_mobile/PP-OCRv4_mobile_det_infer")),
                       ModelModule("PP-OCRv4_mobile_rec", getpath("models/PP-OCRv4_mobile/PP-OCRv4_mobile_rec_infer")))
    PP_OCRV5_MOBILE = (ModelModule("PP-OCRv5_mobile_det", getpath("models/PP-OCRv5_mobile/PP-OCRv5_mobile_det_infer")),
                       ModelModule("PP-OCRv5_mobile_rec", getpath("models/PP-OCRv5_mobile/PP-OCRv5_mobile_rec_infer")))
    PP_OCRV5_SERVER = (ModelModule("PP-OCRv5_server_det", getpath("models/PP-OCRv5_server/PP-OCRv5_server_det_infer")),
                       ModelModule("PP-OCRv5_server_rec", getpath("models/PP-OCRv5_server/PP-OCRv5_server_rec_infer")))

    def __new__(cls, det: ModelModule, rec: ModelModule):
        obj = object.__new__(cls)
        obj.det = det
        obj.rec = rec
        return obj

    @classmethod
    def get_byname(cls, name):
        for model in cls:
            if model.name == name:
                return model
        return None
