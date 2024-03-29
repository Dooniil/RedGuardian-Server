from pydantic import BaseModel


class HostModel(BaseModel):
    ip: str | None
    description: str | None
    groups: list[int] | None
    dns: str | None
    family: int | None
    cpe: str | None

class GroupModel(BaseModel):
    name: str | None
    description: str | None
    host_id_list: list[int] | None

class HostModelHD(BaseModel):
    groups: list[int] | None
# class CredentialModelOptional(BaseModel):
#     name: Optional[str] = None
#     login: Optional[str] = None
#     password: Optional[bytes] = None


