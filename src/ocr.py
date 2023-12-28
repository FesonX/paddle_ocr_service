import base64
import cv2

import numpy as np
from paddleocr import PaddleOCR


class PaddleOCRHanler:
    def __init__(self):
        self.paddle_ocr = PaddleOCR(use_angle_cls=True)

    def ocr_image(self, img_b64: str):
        img = base64.b64decode(img_b64)
        img = np.fromstring(img, np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)

        res = self.paddle_ocr.ocr(img)
        return res

    def get_ocr_text(self, img_b64: str):
        res = self.ocr_image(img_b64)
        return self._format_ocr_result(res)

    def _format_ocr_result(self, res):
        text = ""
        for i in res[0]:
            pos, t = i
            # Avoid token adhesion
            text += f",{t[0]}"
        return text
