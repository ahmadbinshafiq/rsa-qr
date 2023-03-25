from typing import Any

import numpy as np
import qrcode
from pyzbar.pyzbar import decode
from qrcode.image.pil import PilImage

from utils.text import TextUtils


class QR:

    @staticmethod
    def generate_qr(data) -> PilImage:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        return img

    @staticmethod
    def read_qr(img: np.ndarray) -> Any:
        barcodes = decode(img)
        data = barcodes[0].data.decode("utf-8")
        return TextUtils.reformat_using_ast(data)

