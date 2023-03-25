from typing import List

from pydantic import BaseModel


class QRModel(BaseModel):
    name: str
    dob: str
    cnic: str
    details: List[str]


class ImageModel(BaseModel):
    qr: str
    