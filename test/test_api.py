import binascii

import requests
import json

from src.core.keys import Decryption
from src.utils.image import ImageUtils


B_URL = 'http://0.0.0.0:8000'
decryption = Decryption(private_key_path="pem/private.pem")


def is_valid_image(image: str) -> bool:
    try:
        ImageUtils.base64_to_image(image)
        return True
    except binascii.Error:
        return False


def test_qr_api_with_both_enc_and_dec():
    data = {
        "name": "ahmad",
        "dob": "01-Jan-2023",
        "cnic": 10012155.78452,
        "details": ["M", "Asian", "Pakistani"]
    }
    data_json = json.dumps(data)

    res = requests.post(B_URL + '/qr/generate', data=data_json)
    assert res.status_code == 200
    res = res.json()
    assert is_valid_image(res['qr'])

    post_data = {"qr": res['qr']}
    post_data_json = json.dumps(post_data)
    res = requests.post(B_URL + '/qr/read', data=post_data_json)
    assert res.status_code == 200
    res = res.json()
    assert res == data
