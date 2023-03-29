import os
import shutil

import pytest
from Crypto.PublicKey.RSA import RsaKey

from src.core.keys import GenerateKey, SaveKey, LoadKeys, Encryption, Decryption


def test_generate_key_pair():
    private_key, public_key = GenerateKey.generate_key_pair()
    assert private_key is not None
    assert public_key is not None
    assert isinstance(private_key, RsaKey)
    assert isinstance(public_key, RsaKey)


@pytest.mark.parametrize(
    "private_key_path, public_key_path",
    [
        ("pem/private.pem", "pem/public.pem"),
        ("pem/private-file.pem", "pem/public-file.pem"),
        ("pemtest/private.pem", "pemtest/public.pem"),
        ("pem1/private-file.pem", "pem2/public-file.pem")
    ]
)
def test_save_key_pair(private_key_path, public_key_path):
    SaveKey.save_key_pair(
        private_key_path=private_key_path,
        public_key_path=public_key_path
    )
    assert os.path.exists(private_key_path)
    assert os.path.exists(public_key_path)

    # Clean up
    shutil.rmtree(os.path.dirname(private_key_path), ignore_errors=True)
    shutil.rmtree(os.path.dirname(public_key_path), ignore_errors=True)

    assert not os.path.exists(private_key_path)
    assert not os.path.exists(public_key_path)

    # creating default pem files
    SaveKey.save_key_pair()


def test_load_key():
    load_keys = LoadKeys()
    load_keys.load_key("pem/private.pem")
    assert load_keys.key is not None
    assert isinstance(load_keys.key, RsaKey)


@pytest.mark.parametrize(
    "message",
    [
        "Hello World",
        123,
        123.456,
        True
    ]
)
def test_encryption_decryption(message):
    encryption = Encryption()
    decryption = Decryption()

    encrypted_message = encryption.convert(message)
    assert encrypted_message is not None
    assert isinstance(encrypted_message, bytes)

    decrypted_message = decryption.convert(encrypted_message)
    assert decrypted_message is not None
    assert isinstance(decrypted_message, str)
