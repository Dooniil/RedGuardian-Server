from db.entities.Scan_result import ScanResult
from db.entities.Host import Host


class ResultAnalyzer:
    @staticmethod
    async def host_discovery_result_analyze(task_result_id: int, result_info: dict) -> list:
        for host, settings in result_info.items():
            scan_dict = {'task_result_id': task_result_id}
            host_instance = await Host.get_host_by_ip(host)
            if host_instance:
               scan_dict.update(host_id=host_instance.id)

            custom_result = {'ip': host}
            # if settings.get('osmatch'):
            #     os_list = settings.get('osmatch')[0]
            #     os_dict = {}
            #     custom_result.update(os_info=)
            # if settings.get('ports'):
            #     ...
            if settings.get('hostname'):
                custom_result.update(dns=settings.get('hostname')[0].get('name'))
            if settings.get('macaddress'):
                custom_result.update(mac=settings.get('macaddress').get('addr'))
            if settings.get('state'):
                custom_result.update(type_response=settings.get('state').get('reason'))

            scan_dict.update(custom_result=custom_result)

            await ScanResult.create(**scan_dict)
