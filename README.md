This repository contains a custom Ansible Collection, `mahdishariatzade.my_ansible_modules`, featuring two modules:
- **`sqlite_editor`**: A module to read from and write to SQLite databases using SQL queries.
- **`json_editor`**: A module to edit JSON data, including nested structures, using JSONPath expressions.

These modules are designed to simplify database and JSON manipulation tasks in your Ansible playbooks.

## Prerequisites
- **Ansible**: Version 2.9.0 or higher.
- **Python**: Required for running Ansible and the modules.
- **jsonpath-rw**: Required for the `json_editor` module. Install it with:
  ```bash
  pip install jsonpath-rw
  ```
## install:
- `ansible-galaxy collection install mahdishariatzade.sqlite_json_module`
