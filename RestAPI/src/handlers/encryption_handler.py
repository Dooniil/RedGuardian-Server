from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os
from RestAPI.src.encryption import EncyptionManager


def gen_keys(size: int) -> dict:
    #  Генерация ключей без пароля
    private_key: rsa.RSAPrivateKey = rsa.generate_private_key(public_exponent=65537, key_size=size)
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = private_key.public_key()
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    path_folder = os.sep.join([os.getcwd(), 'RestAPI', 'encry_src'])

    path_public = os.sep.join([path_folder, 'public.pem'])
    path_private = os.sep.join([path_folder, 'private.pem'])

    if not os.path.exists(path_folder):
        os.mkdir(path_folder)

    #  Запись ключей в файл
    try:
        with open(path_public, 'wb') as f_pub:
            f_pub.write(public_bytes)
        EncyptionManager.get_public_key()

        with open(path_private, 'wb') as f_pr:
            f_pr.write(private_bytes)
        EncyptionManager.get_private_key()

        return {'status': 'Done'}
    except Exception as e:
        return {'status': 'Error', 'error_msg': e}
