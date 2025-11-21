# @description: 
# @author: licanglong
# @date: 2025/11/19 14:27
import os
from concurrent.futures import ProcessPoolExecutor
from typing import Optional

from paddleocr import PaddleOCR

_global_ocr: Optional[PaddleOCR] = None


def _init_ocr(model):
    """
    每个进程只加载一次 OCR 模型
    """
    global _global_ocr
    if _global_ocr is None:
        _global_ocr = PaddleOCR(
            text_detection_model_name=model.det.name,
            text_recognition_model_name=model.rec.name,
            text_detection_model_dir=model.det.path,
            text_recognition_model_dir=model.rec.path,
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False
        )
    return True


def ocr_task(image_path, model):
    """
    进程执行的任务
    """
    global _global_ocr
    if _global_ocr is None:
        _init_ocr(model)
    return _global_ocr.predict(image_path)


def _dummy_task():
    return True


class ProcessPaddleOcrPool:
    """
    CPU 下最推荐的 OCR 池：真正实现多核并行
    """

    def __init__(self, model, pool_size: Optional[int] = None):
        self.model = model
        self.pool_size = pool_size or os.cpu_count()

        self.executor = ProcessPoolExecutor(
            max_workers=self.pool_size,
            initializer=_init_ocr,
            initargs=(model,)
        )
        # ---------- 提前初始化每个子进程 ----------
        # submit 空任务触发 initializer
        futures = [self.executor.submit(_dummy_task) for _ in range(self.pool_size)]
        for f in futures:
            f.result()  # 等待每个进程初始化完成

    def predict(self, img_path: str):
        """
        阻塞调用，也可扩展 async
        """
        future = self.executor.submit(ocr_task, img_path, self.model)
        return future.result()
