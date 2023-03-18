from RestAPI.models.CredentialModel import CredentialModel
from db.entities.Credential import Credential
from RestAPI.src.encryption import encrypt

platform_table = {
    'Linux': 1,
    'Windows': 2
}


class CredentialHandler:

    @staticmethod
    async def create_new_credential(c_type, data: CredentialModel):
        cred_dict = data.dict()
        encrypted_password: bytes = encrypt(cred_dict.get('password'))
        cred_dict.update(platform_id=platform_table.get(c_type), password=encrypted_password)

        try:
            new_instance = await Credential.create(**cred_dict)
        except Exception as e:
            return {'status': 'Error', 'error_msg': e.args}

        return new_instance.get_response()
