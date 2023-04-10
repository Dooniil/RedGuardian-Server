import json
import os
import base64

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import asyncio
import os.path

from ssl_manager import ssl_manager


class EncyptionManager:
    private_key = None
    public_key = None

    @classmethod
    def encrypt(cls, data: bytes) -> bytes | None:
        public_key = serialization.load_pem_public_key(cls.public_key)
        encrypted_data = public_key.encrypt(
            base64.b64encode(data),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(encrypted_data)

# def decrypt(password: str) -> str:
#     path_private = os.sep.join([os.getcwd(), 'RestAPI', 'encry_src', 'private.pem'])
#
#     with open(path_private, "rb") as key_file:
#         private_key = serialization.load_pem_private_key(key_file.read(), password=None)
#
#     decrypted_password: bytes = private_key.decrypt(
#         password.encode('latin-1'),
#         padding.OAEP(
#             mgf=padding.MGF1(algorithm=hashes.SHA256()),
#             algorithm=hashes.SHA256(),
#             label=None
#         )
#     )
#     return decrypted_password.decode('latin-1')
    @classmethod
    async def get_private_key(cls):
        path_private = os.sep.join([os.getcwd(), 'RestAPI', 'encry_src', 'private.pem'])
        if os.path.exists(path_private):
            with open(path_private, "rb") as key_file:
                cls.private_key = key_file.read()
        else:
            raise

    @classmethod
    async def get_public_key(cls):
        path_public = os.sep.join([os.getcwd(), 'RestAPI', 'encry_src', 'public.pem'])
        if os.path.exists(path_public):
            with open(path_public, "rb") as key_file:
                cls.public_key = key_file.read()
        else:
            raise

    @classmethod
    async def send_key(cls, addr: str, port: int) -> None:
        try:
            r, w = await asyncio.open_connection(addr, port, ssl=ssl_manager.context)
            w.write(json.dumps({'type': 'key', 'key': cls.private_key.decode(encoding="raw_unicode_escape")}).encode())
            await w.drain()
            response = await r.read(1536)
            if response != b'1':
                raise Exception('The key didn\'t send')
            w.close()
            await w.wait_closed()
        except Exception as e:
            print(e)
