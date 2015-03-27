#!/usr/bin/env python
import os
import sys
import filecmp
import shutil

def refresh():
    if os.path.exists('../DB-old.sql'):
        if filecmp.cmp('../DB.sql', '../DB-old.sql') == False:
            os.system('mysql -u root -pruien9690 < ../DB.sql')
            shutil.copy2('../DB.sql', '../DB-old.sql')
            os.system('python3 manage.py migrate')
    else:
        shutil.copy2('../DB.sql', '../DB-old.sql')
        os.system('mysql -u root -pruien9690 < ../DB.sql')
        os.system('python3 manage.py migrate')

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codegalaxy.settings")

    refresh()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
