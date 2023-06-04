from enum import Enum
from pydantic import BaseModel


class TypeHD(str, Enum):
    Only_host_scan = 'Только поиск хостов'
    OS_identification = 'Определение ОС'
    Port_scan_common = 'Сканирование общих портов'
    Port_scan_all = 'Сканирование всех портов'


class TypeProtocol(Enum):
    TCP = 'TCP'
    ICMP = 'ICMP'
    UDP = 'UDP'


class HostDiscoveryModel(BaseModel):
    subnets: list[str]
    type: TypeHD
    protocols: list[TypeProtocol]
    custom_cmd: str | None

