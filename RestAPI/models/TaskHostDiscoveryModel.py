from enum import Enum
from pydantic import BaseModel


class TypeHD(Enum):
    Only_host_scan = 0
    OS_identification = 1
    Port_scan_common = 2
    Port_scan_all = 3
    Custom = 4


class TypeProtocol(Enum):
    TCP = 0
    ICMP = 1
    UDP = 2


class HostDiscoveryModel(BaseModel):
    subnets: list[str]
    type: TypeHD
    protocols: list[TypeProtocol]
    custom_cmd: str | None

