from db.entities.Host import GroupHosts
from db.entities.Host import Host


class GroupHandler:
    @staticmethod
    async def create_group(group_info):
        name, description, host_list = group_info.dict()

        group = await GroupHosts.create(name=name, description=description)

        if host_list:
            for id in host_list:
                host_instance = await Host.get(id)
                if host_instance:
                    instance = await GroupHosts.get_relationship(id, GroupHosts.hosts)
                    instance.hosts.append(id)

        return group
    
    # TODO: code
    @staticmethod
    async def update_host(host_info):
        pass

    @staticmethod
    async def create_host_by_hd_result(hd_result):
        pass