import os
import sys
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../simple_budget'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simple_budget.settings")

from simple_budget.settings import (BACKUP_PATH, DATABASES)

if not BACKUP_PATH or not os.path.isdir(BACKUP_PATH):
    print "Backup Path does not exist"
    sys.exit()

sql_dump_file = 'accounts.zz50.co.uk.sql'
os.popen('export PGPASSWORD="%s";'
         'psql -U%s -h%s %s -c "VACUUM ANALYZE;" > /dev/null 2>&1' %
         (DATABASES['default']['PASSWORD'], DATABASES['default']['USER'],
          DATABASES['default']['HOST'], DATABASES['default']['NAME'],))

os.popen('export PGPASSWORD="%s";pg_dump -U%s -h%s %s '
         '--inserts --clean > %s/%s' %
         (DATABASES['default']['PASSWORD'], DATABASES['default']['USER'],
          DATABASES['default']['HOST'], DATABASES['default']['NAME'],
          BACKUP_PATH, sql_dump_file))

if not os.path.isfile(BACKUP_PATH + '/' + sql_dump_file):
    print "Error Dumping DB"
    sys.exit()

backup_file = 'accounts.zz50.co.uk_%s.tar.gz' % (datetime.date.today())
os.popen('cd %s;tar -czf %s %s' %
         (BACKUP_PATH, backup_file, sql_dump_file))

os.popen('rm %s/%s' % (BACKUP_PATH, sql_dump_file))