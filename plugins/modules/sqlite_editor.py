#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import sqlite3

DOCUMENTATION = r'''
---
module: sqlite_editor
short_description: Manage SQLite database operations
description:
  - This module allows reading from and writing to an SQLite database using SQL queries.
version_added: "1.0.0"
author:
  - Mahdi Shariat <mahdishariat@outlook.com>
options:
  db_path:
    description: Path to the SQLite database file
    required: true
    type: str
  query:
    description: SQL query to execute
    required: true
    type: str
  params:
    description: Parameters for the SQL query to prevent SQL injection
    required: false
    type: list
    default: []
examples:
  - name: Select from SQLite
    mahdishariatzade.my_ansible_modules.sqlite_editor:
      db_path: "/path/to/db.sqlite"
      query: "SELECT * FROM users WHERE id = ?"
      params: [1]
  - name: Update SQLite
    mahdishariatzade.my_ansible_modules.sqlite_editor:
      db_path: "/path/to/db.sqlite"
      query: "UPDATE users SET name = ? WHERE id = ?"
      params: ["Mahdi", 1]
'''

def main():
    module = AnsibleModule(
        argument_spec=dict(
            db_path=dict(type='str', required=True),
            query=dict(type='str', required=True),
            params=dict(type='list', default=[])
        )
    )

    db_path = module.params['db_path']
    query = module.params['query']
    params = module.params['params']

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)

        if query.strip().upper().startswith('SELECT'):
            result = cursor.fetchall()
            module.exit_json(changed=False, result=result)
        else:
            conn.commit()
            module.exit_json(changed=True, msg="Database updated successfully")
    except Exception as e:
        module.fail_json(msg=f"Error: {str(e)}")
    finally:
        conn.close()

if __name__ == '__main__':
    main()