#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import json
import jsonpath_rw

DOCUMENTATION = r'''
---
module: json_editor
short_description: Edit JSON data including nested structures
description:
  - This module edits JSON data using JSONPath expressions, supporting nested structures.
version_added: "1.0.0"
author:
  - Mahdi Shariat <mahdishariat@outlook.com>
options:
  json_data:
    description: JSON data as a string
    required: true
    type: str
  path:
    description: JSONPath expression to locate the value to edit (e.g., $.store.book[0].title)
    required: true
    type: str
  value:
    description: New value to set at the specified path
    required: true
    type: raw
requirements:
  - jsonpath-rw (Python package)
examples:
  - name: Edit nested JSON
    mahdishariatzade.my_ansible_modules.json_editor:
      json_data: '{"store": {"book": [{"title": "Old Title"}]}}'
      path: "$.store.book[0].title"
      value: "New Title"
'''

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