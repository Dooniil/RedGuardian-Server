from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os
from RestAPI.src.encryption import EncyptionManager
from OpenSSL import crypto
import os


class EncryptionException(Exception):
    pass


def gen_keys(size: int) -> dict:
    try:
    #  Генерация ключей без пароля
        try:
            private_key: rsa.RSAPrivateKey = rsa.generate_private_key(public_exponent=65537, key_size=size)
            private_bytes = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        except Exception:
            raise EncryptionException('Ошибка во время создания приватного ключа')
        try:
            public_key = private_key.public_key()
            public_bytes = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        except Exception:
            raise EncryptionException('Ошибка во время создания публичного ключа')

        path_folder = os.sep.join([os.getcwd(), 'RestAPI', 'encry_src'])

        path_public = os.sep.join([path_folder, 'public.pem'])
        path_private = os.sep.join([path_folder, 'private.pem'])

        try:
            if not os.path.exists(path_folder):
                os.mkdir(path_folder)
        except Exception:
            raise EncryptionException('Ошибка во время создания папки encry_src')

        #  Запись ключей в файл
        try:
            with open(path_public, 'wb') as f_pub:
                f_pub.write(public_bytes)
            EncyptionManager.get_public_key()

            with open(path_private, 'wb') as f_pr:
                f_pr.write(private_bytes)
            EncyptionManager.get_private_key()

            return {'Статус': 'Успешно', 'Сообщение': 'Ключи сгенерированы и назодятся в директории RestAPI/encry_src'}
        except Exception:
            raise EncryptionException('Ошибка при записи ключей в файлы')
    except Exception as e:
        return {'Статус': 'Ошибка', 'Сообщение': e}


KEY_FILE = os.sep.join([os.getcwd(), 'RestAPI', 'encry_src', 'ssl', 'private.key'])
CERT_FILE = os.sep.join([os.getcwd(), 'RestAPI', 'encry_src', 'ssl', 'selfsigned.crt'])


def cert_gen(
    emailAddress="emailAddress",
    commonName="commonName",
    countryName="NT",
    localityName="localityName",
    stateOrProvinceName="stateOrProvinceName",
    organizationName="organizationName",
    organizationUnitName="organizationUnitName",
    serialNumber=0,
    validityStartInSeconds=0,
    validityEndInSeconds=10*365*24*60*60):
    try:
        # create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 4096)
        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = countryName
        cert.get_subject().ST = stateOrProvinceName
        cert.get_subject().L = localityName
        cert.get_subject().O = organizationName
        cert.get_subject().OU = organizationUnitName
        cert.get_subject().CN = commonName
        cert.get_subject().emailAddress = emailAddress
        cert.set_serial_number(serialNumber)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(validityEndInSeconds)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha512')
        with open(CERT_FILE, "wt") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
        with open(KEY_FILE, "wt") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))
        return {'Статус': 'Успешно', 'Сообщение': 'Сертификат и ключ сгенерированы и находятся в директории RestAPI/encry_src/ssl'}
    except Exception as e:
        return {'Статус': 'Ошибка', 'Сообщение': e}