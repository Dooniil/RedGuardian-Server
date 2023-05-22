from db.entities.Host import GroupHosts
from db.entities.Host import Host


class GroupHandler:
    @staticmethod
    async def create_group(group_info):
        name, description, host_list = group_info.dict().values()

        group = await GroupHosts.create(name=name, description=description)

        if host_list:
            for id in host_list:
                host_instance = await Host.get(id)
                if host_instance:
                    group_with_relation = await GroupHosts.get_relationship(id, GroupHosts.hosts)
                    group_with_relation.hosts.append(host_instance)

        return group.repr
    
    @staticmethod
    async def get_group(group_id):
        try:
            return await GroupHosts.get_relationship(group_id, GroupHosts.hosts).repr
        except Exception as e:
            return {'status': 'Error', 'error_msg': e.args}

    # TODO: code
    @staticmethod
    async def update_host(host_info):
        pass

    @staticmethod
    async def create_host_by_hd_result(hd_result):
        pass