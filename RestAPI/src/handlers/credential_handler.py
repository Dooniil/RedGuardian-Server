from datetime import datetime

from RestAPI.models.CredentialModel import CredentialModel, CredentialModelOptional
from db.entities.Credential import Credential
from RestAPI.src.encryption import EncyptionManager

platform_table = {
    'Any': 0,
    'Windows': 1,
    'Linux': 2
}


class CredentialHandler:
    @staticmethod
    async def create_new_credential(c_type, data: CredentialModel):
        cred_dict = data.dict()
        encrypted_login: bytes = EncyptionManager.encrypt(cred_dict.get('login'))
        encrypted_password: bytes = EncyptionManager.encrypt(cred_dict.get('password'))
        cred_dict.update(login=encrypted_login, family=platform_table.get(c_type), password=encrypted_password)

        try:
            new_instance = await Credential.create(**cred_dict)
            return new_instance.repr
        except Exception as e:
            return {'Статус': 'Ошибка', 'Сообщение': e}


    @staticmethod
    async def get_credential(c_id):
        try:
            instance = await Credential.get(c_id)
            return instance.repr
        except Exception as e:
            return {'Статус': 'Ошибка', 'Сообщение': e}


    @staticmethod
    async def get_credential_filter(name, platform_type='Any'):
        name = '' if name is None else name
        platform_id = platform_table.get(platform_type)

        try:
            instances = await Credential.get_filter(
                name, platform_id)
        except Exception as e:
            return {'Статус': 'Ошибка', 'Сообщение': e}

        credentials = []
        for instance in instances:
            credentials.append(instance[0].repr)
        return credentials

    @staticmethod
    async def delete_credential(c_id):
        try:
            await Credential.delete(c_id)
            return {'Статус': 'Завершено', 'Сообщение': f'Учетная запись (id = {c_id}) удалена'}
        except Exception as e:
            return {'Статус': 'Ошибка', 'Сообщение': e}


    @staticmethod
    async def update_credential(c_id: int, data: CredentialModelOptional):
        cred_instance = await Credential.get(c_id)
        cred_dict = cred_instance.repr
        
        for k, v in data.dict().items():
            if v:
                if k == 'login' or k == 'password':
                    v = EncyptionManager.encrypt(v)
                cred_dict[k] = v
        try:
            await Credential.update(c_id, cred_dict)
            return cred_instance.repr
        except Exception as e:
            return {'Статус': 'Ошибка', 'Сообщение': e}
