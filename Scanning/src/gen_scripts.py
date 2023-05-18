from db.entities.Definition import JsonDefinition, ExecDefinition


async def generate_execute_definition():
    for json_def in await JsonDefinition.get_all():
        exec_def = await json_def._data[0].get_relationship(json_def._data[0].id, JsonDefinition.execute_definition)
        if exec_def['status'] == 'Error':
            exec_dict = dict(
                id=json_def._data[0].id,
                family_id=json_def._data[0].family_id
            )

            
            vulnerability_dict = json_def._data[0].json_format.get('definitions')[0]
            criteria_dict = vulnerability_dict.get('criteria')
            operator = criteria_dict.get('operator')
            for criteria in criteria_dict.get('criterias'):
                extend_defs = criteria.get('extend_definition')
                criterion = criteria.get('criterion')
                
            ExecDefinition.create(**exec_dict)

    return 
