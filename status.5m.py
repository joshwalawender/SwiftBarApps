#!/Users/joshw/anaconda3/envs/py39/bin/python
#
# <xbar.title>Ohina Status</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Josh Walawender</xbar.author>
# <xbar.desc>Show the current status of various processes</xbar.desc>
#
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np
import mysql.connector

## ------------------------------------------------------------------------
## Database Checks
## ------------------------------------------------------------------------
def check_for_recent_DB_entries(query):
    try:
        cnx = mysql.connector.connect(user='joshw', password='yGyWZsf3gj3wdJW9Bug8',
                                      host='localhost',
                                      database='ohina')
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    cursor = cnx.cursor()

    end = datetime.utcnow()
    start = end-timedelta(minutes=5)

    cursor.execute(query, (start, end))
    cursor.fetchall()
    recent_count = cursor.rowcount
    ok = recent_count > 0
    return ok, recent_count


weather_query = ("SELECT time FROM Weather "
                 "WHERE time BETWEEN %s AND %s")
powerwall_query = ("SELECT time FROM PowerwallData "
                   "WHERE time BETWEEN %s AND %s")
database_checks = [('Weather', weather_query),
                   ('Powerwall', powerwall_query)]
database_check_results = {}
database_checks_ok = True
ok_count = 0
for name, query in database_checks:
    database_check_results[name] = check_for_recent_DB_entries(query)
    database_checks_ok = database_checks_ok and database_check_results[name][0]
    if database_check_results[name][0] == True:
        ok_count += 1



## ------------------------------------------------------------------------
## Backup Checks
## ------------------------------------------------------------------------
def check_age_of_backup(location, backup_age_threshold=2.0):
    location = Path(location)
    try:
        with open(location / '.last_backup_begin', 'r') as f:
            lines = f.readlines()
        lastbegin = datetime.strptime(lines[-1][:16], '%Y%m%dat%H%M%S')
        with open(location / '.last_backup_end', 'r') as f:
            lines = f.readlines()
        last = datetime.strptime(lines[-1][:16], '%Y%m%dat%H%M%S')
        begin_age = (datetime.now()-lastbegin).total_seconds()/60/60/24
        age = (datetime.now()-last).total_seconds()/60/60/24
        ok = age <= backup_age_threshold
    except:
        ok = False
        age = -1
        begin_age = -1
    return ok, age, begin_age


locations = [('Ohina2External/Archive', '/Volumes/Ohina2External/Archive'),
             ('Ohina2External/Astrophotography', '/Volumes/Ohina2External/Astrophotography'),
             ('Ohina2External/Home', '/Volumes/Ohina2External/Home'),
             ('Ohina2External/Lightroom', '/Volumes/Ohina2External/Lightroom'),
             ('Ohina2External/Lightroom Backups', '/Volumes/Ohina2External/Lightroom Backups'),
             ('Ohina2External/Presentations', '/Volumes/Ohina2External/Presentations'),
             ('Ohina2ExternalScienceData', '/Volumes/Ohina2External/ScienceData'),
             ('Ohina2External/Work', '/Volumes/Ohina2External/Work'),
#              ('Ohina2External', '/Volumes/Ohina2External/'),
             ('HarrietDiskStation', '/Volumes/Ohina2External/Backup_HarrietDiskStation/')]
backup_check_results = {}
backup_checks_ok = True
for name, location in locations:
    ok, age, begin_age = check_age_of_backup(location)
    backup_check_results[name] = (ok, age, begin_age)
    backup_checks_ok = backup_checks_ok and ok
    if ok == True:
        ok_count += 1



## ------------------------------------------------------------------------
## Build Overall Status Report
## ------------------------------------------------------------------------
ok = database_checks_ok and backup_checks_ok
ok_string = {True: 'OK', False: 'ALERT'}
total_statuses = len(database_check_results) + len(backup_check_results)

result_string = f"Ohina: {ok_string[ok]}"
if not ok:
    result_string += f' ({total_statuses-ok_count}/{total_statuses})'
print(result_string)
print('---')
for name in database_check_results.keys():
    ok, recent_count = database_check_results[name]
    print(f"{ok_string[ok]}: {name} Entries ({recent_count})")
for name in backup_check_results.keys():
    ok, age, begin_age = backup_check_results[name]
    print(f"{ok_string[ok]}: {name}: age = {age:.1f} days (last attempt: {begin_age:.1f} days)")
