from typing import Optional

from pydantic import BaseModel
from enum import Enum


class Platform(str, Enum):
    Windows = 'Windows',
    Linux = 'Linux',


class PlatformOptional(str, Enum):
    Any = 'Any'
    Windows = 'Windows',
    Linux = 'Linux',


class CredentialModel(BaseModel):
    name: str
    login: bytes
    password: bytes


class CredentialModelOptional(BaseModel):
    name: Optional[str] = None
    login: Optional[bytes] = None
    password: Optional[bytes] = None
    family: Optional[int] = None


