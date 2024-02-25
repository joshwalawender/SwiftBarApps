#!/Users/joshw/anaconda3/envs/py39/bin/python
#
# <xbar.title>Ohina Status</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Josh Walawender</xbar.author>
# <xbar.desc>Show the current status of various processes</xbar.desc>
#
from datetime import datetime, timedelta
import mysql.connector

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

# Weather
weather_query = ("SELECT time FROM Weather "
                 "WHERE time BETWEEN %s AND %s")
end = datetime.utcnow()
start = end-timedelta(minutes=5)
cursor.execute(weather_query, (start, end))
cursor.fetchall()
recent_weather_count = cursor.rowcount
weather_ok = recent_weather_count > 0

# Powerwall
powerwall_query = ("SELECT time FROM PowerwallData "
                   "WHERE time BETWEEN %s AND %s")
cursor.execute(powerwall_query, (start, end))
cursor.fetchall()
recent_powerwall_count = cursor.rowcount
powerwall_ok = recent_powerwall_count > 0


# Backup Ohina2External
backup_age_threshold = 2.0 #days
with open('/Volumes/Ohina2External/.last_backup_begin', 'r') as f:
    lines = f.readlines()
lastbegin = datetime.strptime(lines[-1][:16], '%Y%m%dat%H%M%S')
with open('/Volumes/Ohina2External/.last_backup_end', 'r') as f:
    lines = f.readlines()
last = datetime.strptime(lines[-1][:16], '%Y%m%dat%H%M%S')
O2E_begin_age = (datetime.now()-lastbegin).total_seconds()/60/60/24
O2E_age = (datetime.now()-last).total_seconds()/60/60/24
O2E_ok = O2E_age <= backup_age_threshold

# Backup HarrietDiskStation
backup_age_threshold = 2.0 #days
with open('/Volumes/Ohina2External/Backup_HarrietDiskStation/.last_backup_begin', 'r') as f:
    lines = f.readlines()
lastbegin = datetime.strptime(lines[-1][:16], '%Y%m%dat%H%M%S')
with open('/Volumes/Ohina2External/Backup_HarrietDiskStation/.last_backup_end', 'r') as f:
    lines = f.readlines()
last = datetime.strptime(lines[-1][:16], '%Y%m%dat%H%M%S')
HDS_begin_age = (datetime.now()-lastbegin).total_seconds()/60/60/24
HDS_age = (datetime.now()-last).total_seconds()/60/60/24
HDS_ok = HDS_age <= backup_age_threshold

# Determine overall Ok Status
ok = weather_ok and powerwall_ok and O2E_ok and HDS_ok
ok_count = weather_ok + powerwall_ok + O2E_ok + HDS_ok
ok_string = {True: 'OK', False: 'ALERT'}
total_statuses = 4

# Build output
result_string = f"Ohina: {ok_string[ok]}"
if not ok:
    result_string += f' ({total_statuses-ok_count}/{total_statuses})'
print(result_string)
print('---')
print(f"{ok_string[weather_ok]}: Weather Entries ({recent_weather_count})")
print(f"{ok_string[powerwall_ok]}: Powerwall Entries ({recent_powerwall_count})")
print(f"{ok_string[O2E_ok]}: Ohina2External: age = {O2E_age:.1f} days (last attempt: {O2E_begin_age:.1f} days)")
print(f"{ok_string[HDS_ok]}: HarrietDiskStation: age = {HDS_age:.1f} days (last attempt: {HDS_begin_age:.1f} days)")
