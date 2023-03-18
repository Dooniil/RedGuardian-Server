from pydantic import BaseModel
from enum import Enum


class Platform(str, Enum):
    Linux = 'Linux',
    Windows = 'Windows',


class CredentialModel(BaseModel):
    name: str
    login: str
    password: bytes

