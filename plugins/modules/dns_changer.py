#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import shutil
import os

def main():
    # تعریف پارامترهای ماژول
    module = AnsibleModule(
        argument_spec=dict(
            set_dns=dict(type='bool', default=True),
            restore_dns=dict(type='bool', default=False),
            new_dns=dict(type='list', elements='str', default=[])
        ),
        supports_check_mode=True
    )

    # دریافت پارامترها
    set_dns = module.params['set_dns']
    restore_dns = module.params['restore_dns']
    new_dns = module.params['new_dns']

    # مسیر فایل‌ها
    resolv_conf = '/etc/resolv.conf'
    backup_file = '/etc/resolv.conf.bak'

    # متغیرهای خروجی
    changed = False
    message = []

    # بررسی اینکه هر دو گزینه همزمان فعال نباشند
    if set_dns and restore_dns:
        module.fail_json(msg="نمی‌توان همزمان DNS را تنظیم و بازیابی کرد.")

    # تنظیم DNS جدید
    if set_dns:
        if not new_dns:
            module.fail_json(msg="لیست new_dns خالی است. حداقل یک سرور DNS وارد کنید.")

        # بکاپ گرفتن از فایل فعلی
        if os.path.exists(resolv_conf):
            shutil.copy2(resolv_conf, backup_file)
            message.append(f"فایل {resolv_conf} به {backup_file} بکاپ شد.")
        else:
            message.append(f"فایل {resolv_conf} وجود ندارد، بکاپی ایجاد نشد.")

        # تولید محتوای جدید
        content = "\n".join([f"nameserver {dns}" for dns in new_dns]) + "\n"

        # نوشتن محتوای جدید
        if not module.check_mode:  # در حالت check_mode تغییری اعمال نمی‌شود
            with open(resolv_conf, 'w') as f:
                f.write(content)
        message.append(f"DNS جدید تنظیم شد: {', '.join(new_dns)}")
        changed = True

    # بازیابی DNS قبلی
    if restore_dns:
        if os.path.exists(backup_file):
            if not module.check_mode:  # در حالت check_mode تغییری اعمال نمی‌شود
                shutil.copy2(backup_file, resolv_conf)
            message.append(f"فایل {resolv_conf} از {backup_file} بازیابی شد.")
            changed = True
        else:
            module.fail_json(msg=f"فایل بکاپ {backup_file} وجود ندارد. بازیابی ممکن نیست.")

    # بازگشت نتایج به Ansible
    module.exit_json(changed=changed, message="; ".join(message))

if __name__ == '__main__':
    main()