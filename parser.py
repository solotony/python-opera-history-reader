"""
read Opera browswer history file into .csv

Opera browswer history file is sqlite database
time is stored in microseconds from 01.01.1601 UTC

"""

import sqlite3
import os
import datetime
from dateutil import tz
import pytz
from_zone = tz.gettz('UTC')
tzmsk = pytz.timezone('Europe/Moscow')

def date_from_webkit(webkit_timestamp):
    epoch_start = datetime.datetime(1601,1,1).replace(tzinfo=from_zone).astimezone(tz=tzmsk)
    delta = datetime.timedelta(microseconds=int(webkit_timestamp))
    return epoch_start + delta

#OPERA_PATH = "C:\\Users\\Anton\\AppData\\Roaming\\Opera Software\\Opera Stable\\"
OPERA_PATH = "."
OPERA_HISTORY_FILE = "History"
OPERA_HISTORY_PATH = os.path.join(OPERA_PATH, OPERA_HISTORY_FILE)

conn = sqlite3.connect(OPERA_HISTORY_PATH) # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
for name in res:
    cursor = conn.execute('select * from %s' % name)
    names = list(map(lambda x: x[0], cursor.description))
    print('Table %s' % name)
    print(names)

with open('time.csv', mode='w', encoding='utf-8-sig') as fout:
    for row in conn.execute('SELECT visits.*, '
                            'urls.*, '
                            'visits.visit_time as "d [date]" '
                            'FROM visits  '
                            'LEFT JOIN urls ON visits.url=urls.id '
                            'ORDER BY visits.visit_time'):
        name = row[10][:60].replace(';', ',')
        url = row[9][:60].replace(';', ',')

        #print(';'.join([date_from_webkit(row[2]).strftime("%Y-%m-%d %H:%M"), name,url]))

        print(';'.join([date_from_webkit(row[2]).strftime("%Y-%m-%d %H:%M"),name,url]), file=fout)

exit(0)
