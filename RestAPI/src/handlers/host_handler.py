from db.entities.Host import Host
from db.entities.Host import GroupHosts

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
                instance = await GroupHosts.get_relationship(id, GroupHosts.hosts)
                instance.hosts.append(host.id)

        return host
    
    # TODO: code
    @staticmethod
    async def update_host(host_info):
        pass

    @staticmethod
    async def create_host_by_hd_result(hd_result):
        pass