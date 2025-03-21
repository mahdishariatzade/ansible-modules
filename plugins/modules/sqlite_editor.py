#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import sqlite3

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