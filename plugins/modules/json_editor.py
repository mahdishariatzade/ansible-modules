#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import json
import jsonpath_rw

def set_json_value(json_data, path, value):
    expr = jsonpath_rw.parse(path)
    for match in expr.find(json_data):
        if isinstance(match.value, dict):
            match.value.update(value)
        else:
            match.full_path.update(json_data, value)
    return json_data

def main():
    module = AnsibleModule(
        argument_spec=dict(
            json_data=dict(type='str', required=True),
            path=dict(type='str', required=True),
            value=dict(type='raw', required=True)
        )
    )

    json_str = module.params['json_data']
    path = module.params['path']
    value = module.params['value']

    try:
        json_data = json.loads(json_str)
        modified_json = set_json_value(json_data, path, value)
        module.exit_json(changed=True, result=json.dumps(modified_json))
    except Exception as e:
        module.fail_json(msg=f"Error: {str(e)}")

if __name__ == '__main__':
    main()