# @description: 
# @author: licanglong
# @date: 2025/11/19 14:27
import os
import threading
from queue import Queue

from paddleocr import PaddleOCR

from app.configure.ModelConfigure import ModelsEnum


# config = paddle.inference.Config()
# config.set_mkldnn_cache_capacity(10)


class PaddleOcrPool:
    """
    多模型独立池（Multiton）
    - 每种模型对应一个独立的池
    - 每个池可指定 pool_size
    - 线程安全
    """
    _instances = {}
    _instances_lock = threading.Lock()

    def __new__(cls, model: ModelsEnum, pool_size: int = os.cpu_count()):
        with cls._instances_lock:
            if model not in cls._instances:
                instance = super().__new__(cls)
                cls._instances[model] = instance
            return cls._instances[model]

    def __init__(self, model: ModelsEnum, pool_size: int = os.cpu_count()):
        # 如果已经初始化过该池，不重复创建
        if hasattr(self, "_initialized") and self._initialized:
            return

        # 第一次初始化
        self.model = model
        self.pool_size = pool_size
        self.pool = Queue(maxsize=pool_size)

        for _ in range(pool_size):
            self.pool.put(self._create_ocr())

        self._lock = threading.Lock()
        self._initialized = True

    def _create_ocr(self):
        """创建 PaddleOCR 实例"""
        return PaddleOCR(
            text_detection_model_name=self.model.det.name,
            text_recognition_model_name=self.model.rec.name,
            text_detection_model_dir=self.model.det.path,
            text_recognition_model_dir=self.model.rec.path,
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            # enable_mkldnn=False  # 会降低效率两到三倍
        )

    def predict(self, inp: any):
        """从池中取 OCR 执行预测"""
        ocr = self.pool.get()
        try:
            return ocr.predict(inp)
        finally:
            self.pool.put(ocr)
