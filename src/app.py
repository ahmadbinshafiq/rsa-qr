from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from src.core.keys import Encryption, Decryption
from src.core.qr import QR
from src.models import QRModel, ImageModel
from src.utils.image import ImageUtils
from src.utils.parse import ParsingUtils


app = FastAPI(title="QR", docs_url="/docs")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

encryption = Encryption(public_key_path="pem/public.pem")
decryption = Decryption(private_key_path="pem/private.pem")


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.post("/qr/generate")
async def generate_qr_code(qr: QRModel, response: Response):
    """
    Encrypt the data and generate a QR code.
    :param qr: The data to encrypt.
    :param response: The response objects.
    :return: The QR code.
    """
    enc_data = ParsingUtils.parse_object(qr.dict(), encryption)
    qr = QR.generate_qr(enc_data)
    qr = ImageUtils.image_to_base64(qr)

    response.status_code = 200
    return {"qr": qr}


@app.post("/qr/read")
async def read_qr_code(qr: ImageModel, response: Response):
    """
    Read the QR code and decrypt the data.
    :param qr: The QR code to read.
    :param response: The response objects.
    :return: The decrypted data.
    """
    image = ImageUtils.base64_to_image(qr.qr)
    qr_data = QR.read_qr(image)
    dec_data = ParsingUtils.parse_object(qr_data, decryption)

    response.status_code = 200
    return dec_data

