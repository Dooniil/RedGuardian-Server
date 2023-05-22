from db.entities.Definition import JsonDefinition, ExecDefinition


async def generate_execute_definition():
    count = 0
    for json_def in await JsonDefinition.get_all():
        exec_def = (await json_def._data[0].get_relationship(json_def._data[0].id, JsonDefinition.execute_definition)).repr
        if not exec_def.get('execute_definition'):
            if exec_def.get('family') != 1:
                continue
            exec_dict = dict(
                json_definition_id=json_def._data[0].id,
                family=json_def._data[0].family,
                scripts=list()
            )

            class_def = json_def._data[0].json_format.get('definitions')[0].get('class')
            if class_def == 'vulnerability':
                exec_dict.update(type_def=1)
            elif class_def == 'patch':
                exec_dict.update(type_def=2)
                
            def_class_dict = json_def._data[0].json_format.get('definitions')[0]
            inventory_list = json_def._data[0].json_format.get('definitions')[1:]
            tests_list = json_def._data[0].json_format.get('tests')
            objects_list = json_def._data[0].json_format.get('objects')
            states_list = json_def._data[0].json_format.get('states')
            variables_dict = json_def._data[0].json_format.get('variables')

            criteria_dict = def_class_dict.get('criteria')
            if criteria_dict.get('operator'):
                exec_dict['scripts'].append(criteria_dict.get('operator'))
            
            
            for criteria in criteria_dict.get('criterias'):
                vuln_check = dict(tests=list())
                os_check = dict(tests=list())
                if criteria_dict.get('extend_definition'):
                    extend_defs = criteria_dict.get('extend_definition')
                    vuln_check.update(operator=criteria.get('operator'))
                else:
                    extend_defs = criteria.get('extend_definition')
                    if criteria.get('operator'):
                        os_check.update(operator=criteria.get('operator'))
                
                criterion_list = criteria.get('criterion')
                
                for extend_def in extend_defs:
                    extend_list = list()
                    extend_list.append(extend_def)
                    os_check['tests'].append(await deep_recursive(extend_list, inventory_list, tests_list, objects_list, states_list, variables_dict))
                for criterion_dict in criterion_list:
                    _, vuln_check_result = await get_cmd_from_tests(criterion_dict, tests_list, objects_list, states_list, variables_dict)
                    vuln_check['tests'].append(vuln_check_result)
                '''
                Если у нас несколько тестов, то нужно взять оператор и запихнуть vuln_check как листы
                '''
                exec_dict['scripts'].append(dict(os_check=os_check, vuln_check=vuln_check))
                            
                
            await ExecDefinition.create(**exec_dict)
            count += 1

    return count

async def get_cmd_from_tests(criterion, tests_list, objects_list, states_list, variables_dict):
    get_item_property_cmd = None
    get_item_property_cmd_var = None
    get_version_file_cmd = None
    value_check_operation = None 
    state_value = None
    negate = None
    result_dict = dict(object_cmd_list=list(), state_cmd_list=list())

    for _, info in tests_list.items():
        for test_dict in info:
            negate = True if criterion.get('negate') else False
            if criterion.get('test_ref') == test_dict.get('id'):
                states_test_list = test_dict.get('state')
                state_check_operation =  test_dict.get('check') # TODO: realize

                object_ref = test_dict.get('object')[0].get('object_ref')
                for obj_name, info in objects_list.items():
                    for object_dict in info:
                        if object_ref == object_dict.get('id'):
                            if obj_name == 'family_object':
                                # get_item_property_cmd = f'(Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion").ProductName'
                                result_dict['object_cmd_list'].append(None)
                                break
                            elif obj_name == 'registry_object':
                                obj_hive = 'HKLM:' if object_dict.get('hive') == 'HKEY_LOCAL_MACHINE' else 'HKCU:'
                                obj_key = object_dict.get('key')
                                obj_name = object_dict.get('name')
                                object_path = f'{obj_hive}\{obj_key}'
                                get_item_property_cmd = f'(Get-ItemProperty -Path "{object_path}").{obj_name}'
                                result_dict['object_cmd_list'].append(get_item_property_cmd)
                                break
                            elif obj_name == 'file_object':
                                var_ref = (object_dict.get('path')).get('var_ref')
                                for var_dict in variables_dict.get('local_variable'):
                                    if var_ref == var_dict.get('id'):
                                        object_var_ref = (var_dict.get('object_component')).get('object_ref')
                                        for object_var_dict in objects_list.get('registry_object'):
                                            if object_var_ref == object_var_dict.get('id'):
                                                obj_var_hive = 'HKLM:' if object_var_dict.get('hive') == 'HKEY_LOCAL_MACHINE' else 'HKCU:'
                                                obj_var_key = object_var_dict.get('key')
                                                obj_var_name = object_var_dict.get('name')
                                                object_var_path = f'{obj_var_hive}\{obj_var_key}'
                                                get_item_property_cmd_var = f'(Get-ItemProperty -Path "{object_var_path}").{obj_var_name}'
                                                result_dict['object_cmd_list'].append(get_item_property_cmd_var)
                                                break
                                        literal_component = var_dict.get('literal_component')
                                # else:
                                #     continue
                                # break

                                filename = object_dict.get('filename')
                                get_version_file_cmd = ['(Get-Item', literal_component, filename, ').VersionInfo.ProductVersion']
                                result_dict['object_cmd_list'].append(get_version_file_cmd)
                                break
                    else:
                        continue
                    break

                for state in states_test_list:  # стейты теста
                    state_ref = state.get('state_ref')
                    for _, state_list in states_list.items():  # стейты все
                        for state_dict in state_list:
                            if state_ref == state_dict.get('id'):

                                # state_check_operation =  test_dict.get('check')
                                value_check_operation = state_dict.get('operation') if state_dict.get('operation') else 'equals'
                                state_value = state_dict.get('value')
                                
                                # result_dict['state_cmd_dict']['operator'] = state_check_operation 
                                result_dict['state_cmd_list'].append(dict(operator=value_check_operation, value=state_value))
                                break
                        else:
                            continue
                        break            

    return negate, result_dict
        


async def deep_recursive(extend_defs, inventory_list, tests_list, objects_list, states_list, variables_dict, inventory_dict=None):
    result_list = list()
    for extend_def in extend_defs:
        for inventory_dict in inventory_list:
            if extend_def.get('definition_ref') == inventory_dict.get('id'):
                extend_defs_deep = (inventory_dict.get('criteria')).get('extend_definition')
                if extend_defs_deep:
                    results = await deep_recursive(extend_defs_deep, inventory_list, tests_list, objects_list, states_list, variables_dict, inventory_dict=inventory_dict)
                    result_list.extend(results)
                    

                criterias_list = (inventory_dict.get('criteria')).get('criterias') # add criterias
                if not criterias_list:
                    criterion_list = (inventory_dict.get('criteria')).get('criterion')
                    for criterion in criterion_list:
                        negate, test = await get_cmd_from_tests(criterion, tests_list, objects_list, states_list, variables_dict) # need result 
                        result_list.append(dict(cpe=(inventory_dict.get('metadata')).get('reference')[0].get('ref_id'), test=dict(negate=negate, script=test)))   
                else:
                    for criterias in criterias_list:
                        for criterion in criterias.get('criterion'):
                            negate, test = await get_cmd_from_tests(criterion, tests_list, objects_list, states_list, variables_dict) # need result 
                            result_list.append(dict(cpe=(inventory_dict.get('metadata')).get('reference')[0].get('ref_id'), test=dict(negate=negate, script=test)))           
                
    return result_list