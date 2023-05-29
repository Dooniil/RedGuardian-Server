from fastapi import APIRouter, Query
from RestAPI.src.handlers.encryption_handler import gen_keys, cert_gen

encryption_router = APIRouter(prefix='/encryption', tags=['Шифрование'])


@encryption_router.post('/keys', description='Создание приватного и открытого ключа для шифрования учетных данных.')
async def create_keys(size: int = Query(
    2048, 
    description='Размер ключа. Чем больше значение, тем надежнее ключ, но дольше процесс расшифровки.')
    ):
    res_msg = gen_keys(size)
    return res_msg

@encryption_router.post('/cert', description='Создание сертификата и ключа для работы TLS при передаче данных между компонентами. Алгоритм SHA-512. Для работы TSL необходимо перенести сгенерированные сертификат и ключ в директорию исходников службы сканирования')
async def create_cert_tls(
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
    res_msg = cert_gen(
        emailAddress, 
        commonName, 
        countryName, 
        localityName, 
        stateOrProvinceName, 
        organizationName, 
        organizationUnitName, 
        serialNumber,
        validityStartInSeconds,
        validityEndInSeconds)
    return res_msg
