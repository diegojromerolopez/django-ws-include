import base64
from typing import Tuple

from Crypto.Cipher import AES


def encrypt_to_base64_str(key: str, data: str) -> Tuple[str, str, str]:
    cipher = AES.new(key.encode('utf-8'), AES.MODE_EAX)
    encrypted_data, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
    return (
        base64.b64encode(cipher.nonce).decode('ascii'),
        base64.b64encode(encrypted_data).decode('ascii'),
        base64.b64encode(tag).decode('ascii')
    )


def decrypt_from_base64_str(key: str, nonce: str, encrypted_data: str, tag: str) -> str:
    bin_key = key.encode('utf-8')
    bin_nonce = base64.b64decode(nonce.encode('ascii'))
    bin_encrypted_data = base64.b64decode(encrypted_data.encode('ascii'))
    bin_tag = base64.b64decode(tag.encode('ascii'))

    cipher = AES.new(
        bin_key, AES.MODE_EAX, bin_nonce
    )
    data = cipher.decrypt_and_verify(
        bin_encrypted_data, bin_tag
    )
    return data.decode('utf-8')
