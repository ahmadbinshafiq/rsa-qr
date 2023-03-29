import pytest
from qrcode.image.pure import PyPNGImage

from src.core.qr import QR
from src.utils.image import ImageUtils


@pytest.mark.parametrize(
    "data",
    [
        {
            "name": "ahmad",
            "dob": "01-Jan-2023",
            "cnic": "1001215578452",
            "details": ["M", "Asian", "Pakistani"]
        },
        {
            "number": 123,
            "float": 180.5452,
            "list": [25, "abc", 1.235, {"hi": "hello"}],
            "dict": {"hi": "hello"}

        },
        "Hello World!",
        1232,
        1235.2455,
        [1254, "hi", True]
    ]
)
def test_qr_code(data):
    qr = QR.generate_qr(data)
    assert qr is not None
    assert isinstance(qr, PyPNGImage)

    img_str = ImageUtils.image_to_base64(qr)  # convert qr to base64 string
    img = ImageUtils.base64_to_image(img_str)  # convert base64 string to np.ndarray

    decode_qr = QR.read_qr(img)

    assert decode_qr == (str(data) if isinstance(data, int) or isinstance(data, float) else data)

