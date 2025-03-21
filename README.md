# My Ansible Modules

این پروژه شامل دو ماژول سفارشی برای Ansible است:
- `sqlite_editor`: برای خواندن و ویرایش دیتابیس SQLite
- `json_editor`: برای ویرایش داده‌های JSON (با پشتیبانی از ساختارهای تو در تو)

## پیش‌نیازها
- Ansible نسخه 2.9 یا بالاتر
- برای ماژول `json_editor`:
  ```bash
  pip install jsonpath-rw