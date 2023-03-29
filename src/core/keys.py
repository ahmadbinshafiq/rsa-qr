import os
from typing import Union, Tuple
from abc import ABC, abstractmethod

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey.RSA import RsaKey


class GenerateKey:
    """
    Generate RSA key pair
    """

    @staticmethod
    def generate_key_pair(key_size: int = 1024) -> Tuple[RsaKey, RsaKey]:
        """
        Generate RSA keys, private and public
        :param key_size: Optional, default 1024
        :return: Tuple of private and public keys
        """
        random_generator = Random.new().read
        key_pair = RSA.generate(key_size, random_generator)
        return key_pair, key_pair.publickey()


class SaveKey:
    """
    Save RSA key pair to file system
    """

    @staticmethod
    def save_key_pair(
            private_key_path: str = "pem/private.pem", public_key_path: str = "pem/public.pem", key_size: int = 1024
    ) -> None:
        """
        Save RSA key pair to file system
        :param private_key_path: Optional, default "pem/private.pem"
        :param public_key_path: Optional, default "pem/public.pem"
        :param key_size: Optional, default 1024
        :return: None: Saves RSA key pair to file system
        """
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
    """
    Load RSA key pair from file system
    """

    def __init__(self):
        self._key: Union[RsaKey, None] = None

    def load_key(self, key_path: str):
        """
        Load RSA key from file system
        :param key_path:
        :return: None: Loads RSA key from file system
        """
        with open(key_path, 'rb') as f:
            self._key = RSA.import_key(f.read())

    @property
    def key(self) -> RsaKey:
        """
        Get the RSA key loaded from file system
        :return: RSA key
        """
        return self._key


class EncryptionDecryptionInterface(ABC):
    """
    Interface for encryption and decryption
    """

    @abstractmethod
    def convert(self, message: Union[str, int, float, bool]) -> bytes:
        """Convert message to encrypted message"""
        pass


class Encryption(LoadKeys, EncryptionDecryptionInterface):
    """
    Encrypt message using RSA public key
    """

    def __init__(self, public_key_path: str = "pem/public.pem"):
        super().__init__()
        self.load_key(public_key_path)

    def convert(self, message: Union[str, int, float, bool]) -> bytes:
        """
        Encrypts message using RSA public key
        :param message: Message to be encrypted
        :return: Encrypted message
        """
        cipher = PKCS1_OAEP.new(self._key)
        encrypted_message = cipher.encrypt(str(message).encode('utf-8'))
        return encrypted_message


class Decryption(LoadKeys, EncryptionDecryptionInterface):
    """
    Decrypt message using RSA private key
    """

    def __init__(self, private_key_path: str = "pem/private.pem"):
        super().__init__()
        self.load_key(private_key_path)

    def convert(self, encrypted_message: bytes) -> str:
        """
        Decrypts message using RSA private key
        :param encrypted_message
        :return: Decrypted message
        """
        cipher = PKCS1_OAEP.new(self._key)
        decrypted_message = cipher.decrypt(encrypted_message)
        return decrypted_message.decode('utf-8')
