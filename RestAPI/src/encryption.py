import os
import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization


def encrypt(password: bytes) -> bytes:
    path_public = os.sep.join([os.getcwd(), 'RestAPI', 'encry_src', 'public.pem'])

    with open(path_public, "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())

    encrypted_password = public_key.encrypt(
        base64.b64encode(password),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted_password)

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


def get_private_key():
    path_private = os.sep.join([os.getcwd(), 'RestAPI', 'encry_src', 'private.pem'])

    with open(path_private, "rb") as key_file:
        private_key = key_file.read()
    return private_key
