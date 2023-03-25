import os
from typing import Union, Tuple
from abc import ABC, abstractmethod

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey.RSA import RsaKey


class GenerateKey:

    @staticmethod
    def generate_key_pair(key_size: int = 1024) -> Tuple[RsaKey, RsaKey]:
        random_generator = Random.new().read
        key_pair = RSA.generate(key_size, random_generator)
        return key_pair, key_pair.publickey()


class SaveKey:

    @staticmethod
    def save_key_pair(
            private_key_path: str = "pem/private.pem", public_key_path: str = "pem/public.pem", key_size: int = 1024
    ) -> None:
        private_key, public_key = GenerateKey.generate_key_pair(key_size)

        if not os.path.exists(os.path.dirname(private_key_path)):  # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(private_key_path))
        if not os.path.exists(os.path.dirname(public_key_path)):  # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(public_key_path))

        with open(private_key_path, 'wb') as f:
            f.write(private_key.export_key('PEM'))
        with open(public_key_path, 'wb') as f:
            f.write(public_key.export_key('PEM'))


class LoadKeys:

    def __init__(self):
        self._key: Union[RsaKey, None] = None

    def load_key(self, key_path: str):
        with open(key_path, 'rb') as f:
            self._key = RSA.import_key(f.read())

    @property
    def key(self) -> RsaKey:
        return self._key


class EncryptionDecryptionInterface(ABC):

    @abstractmethod
    def convert(self, message: Union[str, int, float, bool]) -> bytes:
        pass


class Encryption(LoadKeys, EncryptionDecryptionInterface):

    def __init__(self, public_key_path: str = "pem/public.pem"):
        super().__init__()
        self.load_key(public_key_path)

    def convert(self, message: Union[str, int, float, bool]) -> bytes:
        cipher = PKCS1_OAEP.new(self._key)
        encrypted_message = cipher.encrypt(str(message).encode('utf-8'))
        return encrypted_message


class Decryption(LoadKeys, EncryptionDecryptionInterface):

    def __init__(self, private_key_path: str = "pem/private.pem"):
        super().__init__()
        self.load_key(private_key_path)

    def convert(self, encrypted_message: bytes) -> str:
        cipher = PKCS1_OAEP.new(self._key)
        decrypted_message = cipher.decrypt(encrypted_message)
        return decrypted_message.decode('utf-8')
