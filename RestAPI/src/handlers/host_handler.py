from db.entities.Host import Host
from db.entities.Host import GroupHosts
from db.entities.Task_result import TaskResult

class HostHandler:
    @staticmethod
    async def create_host(host_info):
        host_dict = host_info.dict()
        groups = host_dict.get('groups')
        host_dict.pop('groups')

        if host_dict.get('cpe'):
            if 'windows' in host_dict.get('cpe'):
                host_dict.update(family=1)
            elif 'alt' in host_dict.get('cpe'):
                host_dict.update(family=2)
    
        host = await Host.create(**host_dict)
        if groups:
            for id in groups:
                group_with_relation = await GroupHosts.get_relationship(id, GroupHosts.hosts)
                group_with_relation.hosts.append(host)
            await Host.update(host.id, host_dict)
        
        return {'Статус': 'Завершено', 'ID хоста': host.id}

    @staticmethod
    async def create_host_by_hd(task_result_id, groups):
        hosts_id = list()
        task_result_instance = await TaskResult.get_relationship(task_result_id, TaskResult.scan_results)
        for result in task_result_instance.scan_results:
            host_dict = dict(
                ip=result.custom_result['ip'],
                dns=result.custom_result.get('dns')
            )
            if not result.host_id:
                host = await Host.create(**host_dict)
                hosts_id.append(host.id)
                if groups:
                    for id in groups:
                        group_with_relation = await GroupHosts.get_relationship(id, GroupHosts.hosts)
                        group_with_relation.hosts.append(host)
                    await Host.update(host.id, host_dict)
        return {
            'Статус': 'Завершено', 
            'Сообщение': f'Добавлено хостов: {len(hosts_id)}',
            'ID хостов': hosts_id}
    
    @staticmethod
    async def get_host(host_id):
        try:
            instance_dict = (await Host.get_relationship(host_id, Host.groups)).repr
            group_list = list()
            for group in instance_dict.get('groups'):
                group_list.append(dict(id=group.id, name=group.name, description=group.description))
            instance_dict['groups'] = group_list
            return instance_dict
        except Exception as e:
            return {'Cтатус': 'Ошибка', 'Сообщение': e}

    @staticmethod
    async def update_host(host_id, new_host_info_model=None, new_host_info_dict=None):
        host_instance = await Host.get_relationship(host_id, Host.groups)
        host_dict = host_instance.repr

        if new_host_info_model:
            new_host_info = new_host_info.dict()
        elif new_host_info_dict:
            new_host_info = new_host_info_dict

        for k, v in new_host_info.items():
            if v and k != 'groups':
                host_dict[k] = v
        try:
            group_list = new_host_info.dict().get('groups') #  id измененных групп
            if group_list: # если не пустой
                for group in host_dict.get('groups'):
                    if group.id not in group_list:
                        group_with_relation = await GroupHosts.get_relationship(group.id, GroupHosts.hosts)
                        group_with_relation.hosts.remove(host_instance)

                for id in group_list:
                    group_with_relation = await GroupHosts.get_relationship(id, GroupHosts.hosts)
                    if group_with_relation not in host_dict.get('groups'):
                        group_with_relation.hosts.append(host_instance)

                
                        
            else: # если пустой, то удаляем все хосты
                for group in host_dict.get('groups'):
                    group_with_relation = await GroupHosts.get_relationship(group.id, GroupHosts.hosts)
                    group_with_relation.hosts.remove(host_instance)

            host_dict.pop('groups') # чтобы обновить без групп
            await Host.update(host_id, host_dict)
            return {'Статус': 'Завершено'}
        except Exception as e:
            return {'Cтатус': 'Ошибка', 'Сообщение': e}
        
    @staticmethod
    async def delete_host(host_id):
        try:
            await Host.delete(host_id)
            return {'Статус': 'Завершено'}
        except Exception as e:
            return {'Cтатус': 'Ошибка', 'Сообщение': e}
        