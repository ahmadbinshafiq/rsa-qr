import base64
import io
from typing import Union

import cv2
import numpy as np
from qrcode.image.pure import PyPNGImage


class ImageUtils:

    @staticmethod
    def image_to_base64(image: Union[np.ndarray, PyPNGImage]) -> str:
        if isinstance(image, np.ndarray):
            retval, buffer = cv2.imencode('.jpg', image)
            return base64.b64encode(buffer).decode('utf-8')
        elif isinstance(image, PyPNGImage):
            binary_stream = io.BytesIO()
            image.save(binary_stream)
            return base64.b64encode(binary_stream.getvalue()).decode("utf-8")

    @staticmethod
    def base64_to_image(base64_string: str) -> np.ndarray:
        nparr = np.frombuffer(base64.b64decode(base64_string), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return image
