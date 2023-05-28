import os
import base64
from Scanning.scanners_src.request_type import RequestType
from Scanning.scanners_src.sender_messages import SenderMsg
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import os.path


class EncyptionManager:
    private_key = None
    public_key = None

    @classmethod
    def encrypt(cls, data: bytes) -> bytes | None:
        public_key = serialization.load_pem_public_key(cls.public_key)
        encrypted_data = public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(encrypted_data)


    @classmethod
    async def get_private_key(cls):
        path_private = os.sep.join([os.getcwd(), 'RestAPI', 'encry_src', 'private.pem'])
        if os.path.exists(path_private):
            with open(path_private, "rb") as key_file:
                cls.private_key = key_file.read()
        else:
            pass

    @classmethod
    async def get_public_key(cls):
        path_public = os.sep.join([os.getcwd(), 'RestAPI', 'encry_src', 'public.pem'])
        if os.path.exists(path_public):
            with open(path_public, "rb") as key_file:
                cls.public_key = key_file.read()
        else:
            pass

    @classmethod
    async def send_key(cls, host: str, port: int) -> None:
        try:
            key_sender = SenderMsg(host, port)
            request = {
                'type': RequestType.KEY.value,
                'key': cls.private_key.decode(encoding="raw_unicode_escape")
            }
            async with key_sender:
                await key_sender.send_msg(request)
        except Exception as e:
            print(e)
