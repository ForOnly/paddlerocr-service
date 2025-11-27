# @description: 
# @author: licanglong
# @date: 2025/11/20 14:22
import os
from concurrent.futures import ThreadPoolExecutor

import cv2
import numpy as np
from flask import request, jsonify

from app.blueprints.base import base_bp
from app.client.PaddleOcrClient import PaddleOcrPool
from app.configure.ModelConfigure import ModelsEnum
from app.models.Result import SysResult

# 支持的扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@base_bp.route('/ocr', methods=['POST'])
def ocr_endpoint():
    ocr = PaddleOcrPool(ModelsEnum.PP_OCRV5_MOBILE)

    def rec_text(file):
        if file.filename == '' or not allowed_file(file.filename):
            return None
        img_bytes = np.frombuffer(file.read(), np.uint8)
        img_cv = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
        ocr_result = ocr.predict(img_cv)
        return {"ocr_result": [r.json for r in ocr_result]}

    # 文件上传模式
    files = request.files.getlist("files")
    if not files:
        return jsonify(SysResult.fail("No image provided"))
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        results = list(executor.map(lambda x: rec_text(x), files))

    # 处理结果，只返回可序列化的数据
    return jsonify(SysResult.success(data=[result for result in results if result]))
