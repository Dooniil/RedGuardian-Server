from db.entities.Definition import JsonDefinition, ExecDefinition


async def generate_execute_definition():
    for json_def in await JsonDefinition.get_all():
        exec_def = await json_def._data[0].get_relationship(json_def._data[0].id, JsonDefinition.execute_definition)
        if exec_def['status'] == 'Error':
            exec_dict = dict(
                id=json_def._data[0].id,
                family_id=json_def._data[0].family_id,
                scripts=list()
            )

            vulnerability_dict = json_def._data[0].json_format.get('definitions')[0]
            inventory_list = json_def._data[0].json_format.get('definitions')[1:]
            tests_list = json_def._data[0].json_format.get('tests')
            objects_list = json_def._data[0].json_format.get('objects')
            states_list = json_def._data[0].json_format.get('states')
            variables_dict = json_def._data[0].json_format.get('variables')

            criteria_dict = vulnerability_dict.get('criteria')
            operator = criteria_dict.get('operator')
            for criteria in criteria_dict.get('criterias'):
                extend_defs = criteria.get('extend_definition')
                criterion = criteria.get('criterion')

                deep_recursive(extend_defs, inventory_list, tests_list, objects_list, states_list, variables_dict)
                            
                
            ExecDefinition.create(**exec_dict)

    return 

async def get_cmd_from_tests(criterion, tests_list, objects_list, states_list, variables_dict):
    get_item_property_cmd = None
    get_item_property_cmd_var = None
    get_version_file_cmd = None
    value_check_operation = None 
    state_value = None

    result_list = dict(object_cmd_list=list(), state_cmd_dict=dict(operator=None, values=list()))

    for _, info in tests_list.items():
        for test_dict in info:
            if criterion.get('test_ref') == test_dict.get('id'):
                states_test_list = test_dict.get('state')
                state_check_operation =  test_dict.get('check') # TODO: realize

                object_ref = test_dict.get('object')[0].get('object_ref')
                for obj_name, info in objects_list.items():
                    for object_dict in info:
                        if object_ref == object_dict.get('id'):
                            if obj_name == 'registry_object':
                                obj_hive = 'HKLM:' if object_dict.get('hive') == 'HKEY_LOCAL_MACHINE' else 'HKCU:'
                                obj_key = object_dict.get('key')
                                obj_name = object_dict.get('name')
                                object_path = f'{obj_hive}\{obj_key}'
                                result_list['object_cmd_list'].append(get_item_property_cmd = f'(Get-ItemProperty -Path "{object_path}").{obj_name}')
                            elif obj_name == 'file_object':
                                var_ref = (object_dict.get('path')).get('var_ref')
                                for var_dict in variables_dict.get('local_variable'):
                                    if var_ref == var_dict.get('id'):
                                        object_var_ref = (var_dict.get('object_component')).get('object_ref')
                                        for info in objects_list.get('registry_object'):
                                            for object_var_dict in info:
                                                if object_var_ref == object_var_dict.get('id'):
                                                    obj_var_hive = 'HKLM:' if object_var_dict.get('hive') == 'HKEY_LOCAL_MACHINE' else 'HKCU:'
                                                    obj_var_key = object_var_dict.get('key')
                                                    obj_var_name = object_var_dict.get('name')
                                                    object_var_path = f'{obj_var_hive}\{obj_var_key}'
                                                    result_list['object_cmd_list'].append(get_item_property_cmd_var = f'(Get-ItemProperty -Path "{object_var_path}").{obj_var_name}')
                                        literal_component = var_dict.get('literal_component')

                                filename = object_dict.get('filename')
                                result_list['object_cmd_list'].append(get_version_file_cmd = ['(Get-Item', literal_component, filename, ').VersionInfo.ProductVersion'])

                for state in states_test_list:
                    if state.get('state_ref') == states_list.get('id'):
                        states_test_list = test_dict.get('state')
                        state_check_operation =  test_dict.get('check')
                        for state in states_test_list: 
                            for _, info in tests_list.items():
                                for state_dict in info:
                                    if state.get('state_ref') == state_dict.get('id'):
                                        value_check_operation = state_dict.get('operation') if state_dict.get('operation') else 'equals'
                                        state_value = state_dict.get('value')
                    result_list['state_cmd_dict']['operator'] = state_check_operation
                    result_list['state_cmd_dict']['values'] = dict(operator=value_check_operation, value=state_value)
    
    return result_list
        


async def deep_recursive(extend_defs, inventory_list, tests_list, objects_list, states_list, variables_dict):
    result_dict = dict()
    for extend_def in extend_defs:
        for inventory_dict in inventory_list:
            if extend_def.get('definition_ref') == inventory_dict.get('id'):
                extend_defs_deep = (inventory_dict.get('criteria')).get('extend_definition')
                if extend_defs_deep:
                    deep_recursive(extend_defs_deep, inventory_dict)

                criterion_list = (inventory_dict.get('criteria')).get('criterion') # add criterias
                for criterion in criterion_list:
                    tests: list = await get_cmd_from_tests(criterion, tests_list, objects_list, states_list, variables_dict) # need result 
                    result_dict.update(cpe=(inventory_dict.get('metadata')).get('reference')[0].get('ref_id'), tests=tests)                      