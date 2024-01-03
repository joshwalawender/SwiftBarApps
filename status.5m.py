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
powerwall_query = ("SELECT time FROM Powerwall "
                   "WHERE time BETWEEN %s AND %s")
cursor.execute(powerwall_query, (start, end))
cursor.fetchall()
recent_powerwall_count = cursor.rowcount
powerwall_ok = recent_powerwall_count > 0

# Backup ScienceData
with open('/Volumes/Ohina2External/ScienceData/.last_backup_end', 'r') as f:
    lines = f.readlines()
    last = datetime.strptime(lines[-1][:16], '%Y%m%dat%H%M%S')
ScienceData_age = (datetime.now()-last).total_seconds()/60/60/24
ScienceData_ok = ScienceData_age <= 1

# Backup Ohina2External
with open('/Volumes/Ohina2External/.last_backup_end', 'r') as f:
    lines = f.readlines()
    last = datetime.strptime(lines[-1][:16], '%Y%m%dat%H%M%S')
Ohina2External_age = (datetime.now()-last).total_seconds()/60/60/24
Ohina2External_ok = Ohina2External_age <= 1

# Backup HarrietDiskStation
with open('/Volumes/Ohina2External/Backup_HarrietDiskStation/.last_backup_end', 'r') as f:
    lines = f.readlines()
    last = datetime.strptime(lines[-1][:16], '%Y%m%dat%H%M%S')
HarrietDiskStation_age = (datetime.now()-last).total_seconds()/60/60/24
HarrietDiskStation_ok = HarrietDiskStation_age <= 1

ok = weather_ok and powerwall_ok and ScienceData_ok and Ohina2External_ok and HarrietDiskStation_ok
ok_count = weather_ok + powerwall_ok + ScienceData_ok + Ohina2External_ok + HarrietDiskStation_ok
ok_string = {True: 'OK', False: 'ALERT'}
total_statuses = 5

result_string = f"Ohina: {ok_string[ok]}"
if not ok:
    result_string += f' ({total_statuses-ok_count}/{total_statuses})'
print(result_string)
print('---')
print(f"{ok_string[weather_ok]}: Weather Entries ({recent_weather_count})")
print(f"{ok_string[powerwall_ok]}: Powerwall Entries ({recent_powerwall_count})")
print(f"{ok_string[ScienceData_ok]}: Backup ScienceData ({ScienceData_age:.1f} days)")
print(f"{ok_string[Ohina2External_ok]}: Backup Ohina2External ({Ohina2External_age:.1f} days)")
print(f"{ok_string[HarrietDiskStation_ok]}: Backup HarrietDiskStation ({HarrietDiskStation_age:.1f} days)")
