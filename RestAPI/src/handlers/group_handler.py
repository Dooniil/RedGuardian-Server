from db.entities.Host import GroupHosts
from db.entities.Host import Host


class GroupHandler:
    @staticmethod
    async def create_group(group_info):
        name, description, host_list = group_info.dict().values()

        group = await GroupHosts.create(name=name, description=description)

        if host_list:
            for id in host_list:
                host_instance = await Host.get_relationship(id, Host.groups)
                group_with_relation = await GroupHosts.get_relationship(id, GroupHosts.hosts)
                group_with_relation.hosts.append(host_instance)
            await GroupHosts.update(group.id, dict(name=name, description=description))

        return {'status': 'Done', 'group_id': group.id}
    
    @staticmethod
    async def get_group(group_id):
        try:
            instance_dict = (await GroupHosts.get_relationship(group_id, GroupHosts.hosts)).repr
            host_list = list()
            for host in instance_dict.get('hosts'):
                host_list.append(dict(
                    id=host.id, 
                    ip=host.ip, 
                    description=host.description,
                    dns=host.dns,
                    family=host.family,
                    cpe=host.cpe
                    ))
            instance_dict['hosts'] = host_list
            return instance_dict
        except Exception as e:
            return {'status': 'Error', 'error_msg': e.args}

    @staticmethod
    async def update_group(group_id, new_group_info):
        group_with_relation = await GroupHosts.get_relationship(group_id, GroupHosts.hosts)
        group_dict = group_with_relation.repr

        for k, v in new_group_info.dict().items():
            if v and k != 'host_id_list':
                group_dict[k] = v
        try:
            host_list = new_group_info.dict().get('host_id_list') #  id измененных хостов
            if host_list: # если не пустой
                for host in group_dict.get('hosts'):
                    if host.id not in host_list:
                        host_with_relation = await Host.get_relationship(host.id, Host.groups)
                        group_with_relation.hosts.remove(host_with_relation)

                for id in host_list:
                    host_with_relation = await Host.get_relationship(id, Host.groups)
                    if host_with_relation not in group_dict.get('hosts'):
                        group_with_relation.hosts.append(host_with_relation)

            else: # если пустой, то удаляем все хосты
                for host in group_dict.get('hosts'):
                    host_with_relation = await Host.get_relationship(host.id, Host.groups)
                    group_with_relation.hosts.remove(host_with_relation)

            group_dict.pop('hosts') # чтобы обновить без групп
            await GroupHosts.update(group_id, group_dict)
            return {'status': 'Done'}
        except Exception as e:
            return {'status': 'Error', 'error_msg': e.args}

    @staticmethod
    async def delete_group(group_id):
        try:
            await GroupHosts.delete(group_id)
            return {'status': 'Done'}
        except Exception as e:
            return {'status': 'Error', 'error_msg': e.args}
        
    @staticmethod
    async def create_host_by_hd_result(hd_result):
        pass