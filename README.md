This repository contains a custom Ansible Collection, `mahdishariatzade.sqlite_json_module`, featuring two modules:
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
- ```
  ansible-galaxy collection install mahdishariatzade.sqlite_json_module
  ```


## Usage

Below are examples of how to use the `sqlite_editor` and `json_editor` modules in your Ansible playbooks.

### Module: `sqlite_editor`
This module allows you to execute SQL queries on an SQLite database, enabling both reading and writing operations.

#### Parameters
- **`db_path`** (required, string): Path to the SQLite database file.
- **`query`** (required, string): SQL query to execute.
- **`params`** (optional, list, default: `[]`): Parameters for the query to prevent SQL injection.

#### Returns
- For `SELECT` queries: A list of results (`result`).
- For other queries (e.g., `INSERT`, `UPDATE`): A confirmation message (`msg`).

#### Examples
1. **Create a Table and Insert Data**
   ```yaml
   - name: Create a table in SQLite
     mahdishariatzade.sqlite_json_module.sqlite_editor:
       db_path: "/path/to/database.db"
       query: "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, data TEXT)"

   - name: Insert a user with JSON data
     mahdishariatzade.sqlite_json_module.sqlite_editor:
       db_path: "/path/to/database.db"
       query: "INSERT INTO users (id, name, data) VALUES (?, ?, ?)"
       params: [1, "Mahdi", '{"role": "admin", "age": 30}']

#### Combined Example: Edit JSON in SQLite
This example shows how to fetch JSON data from SQLite, edit it, and update the database.

```yaml
- name: Edit JSON in SQLite database
  hosts: localhost
  tasks:
    - name: Fetch JSON data from SQLite
      mahdishariatzade.sqlite_json_module.sqlite_editor:
        db_path: "/path/to/database.db"
        query: "SELECT data FROM users WHERE id = ?"
        params: [1]
      register: db_result

    - name: Edit JSON role
      mahdishariatzade.sqlite_json_module.json_editor:
        json_data: "{{ db_result.result[0][0] }}"
        path: "$.role"
        value: "developer"
      register: json_result

    - name: Update SQLite with modified JSON
      mahdishariatzade.sqlite_json_module.sqlite_editor:
        db_path: "/path/to/database.db"
        query: "UPDATE users SET data = ? WHERE id = ?"
        params: ["{{ json_result.result }}", 1]