from datetime import datetime

from RestAPI.models.CredentialModel import CredentialModel, CredentialModelOptional
from db.entities.Credential import Credential
from RestAPI.src.encryption import encrypt

platform_table = {
    'Any': 0,
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

        return new_instance.repr

    @staticmethod
    async def get_credential(c_id):
        try:
            instance = (await Credential.get(c_id))[0]
        except Exception as e:
            return {'status': 'Error', 'error_msg': e.args}

        return instance.repr

    @staticmethod
    async def get_credential_filter(name, created_date, updated_date, platform_type='Any'):
        name = '' if name is None else name
        created_date = datetime(1991, 1, 1) if created_date is None else created_date
        updated_date = datetime(1991, 1, 1) if updated_date is None else updated_date
        platform_id = platform_table.get(platform_type)

        try:
            instances = await Credential.get_filter(
                name, platform_id, created_date, updated_date)
        except Exception as e:
            return {'status': 'Error', 'error_msg': e.args}

        response = []
        for instance in instances:
            response.append(instance[0].repr)
        return response

    @staticmethod
    async def delete_credential(c_id):
        try:
            await Credential.delete(c_id)

        except Exception as e:
            return {'status': 'Error', 'error_msg': e.args}

        return {'status': 'Done'}

    @staticmethod
    async def update_credential(c_id: int, data: CredentialModelOptional):
        cred_dict = {}
        for k, v in data.dict().items():
            if v:
                cred_dict[k] = v
        try:
            await Credential.update(c_id, cred_dict)
        except Exception as e:
            return {'status': 'Error', 'error_msg': e.args}

        return {'status': 'Done'}
