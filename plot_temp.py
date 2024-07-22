import pandas as pd
import numpy as np
import MySQLdb
import pandas_datareader.data as pdr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import requests

dt_now = datetime.now()
# dt_now = dt_now + timedelta(1)
yesterday = dt_now - timedelta(1)

conn = MySQLdb.connect(user='user_homeHK', password='qAfbUr3rD7i44UihR', host='localhost', database='homeHK')
cur = conn.cursor()
cur.execute("select * from BME680_workroom where date_format(date_and_time,'%Y-%m-%d') = \"" + yesterday.strftime("%Y-%m-%d") + "\" order by date_and_time asc;")

time_array_workroom  = []
temperature_array_workroom = []
pressure_local_array_workroom = []
pressure_sea_array_workroom = []
humidity_array_workroom = []



#終値がゼロ（取引がない）ときを除いて、データを配列に格納する。
for row in cur.fetchall():            
    time_array_workroom.append(row[0]) 
    temperature_array_workroom.append(row[1])
    pressure_local_array_workroom.append(row[2])
    pressure_sea_array_workroom.append(row[3])
    humidity_array_workroom.append(row[4])
    
    
cur.execute("select * from BME680_outside where date_format(date_and_time,'%Y-%m-%d') = \"" + yesterday.strftime("%Y-%m-%d") + "\" order by date_and_time asc;")

time_array_outside  = []
temperature_array_outside = []
pressure_local_array_outside = []
pressure_sea_array_outside = []
humidity_array_outside = []



#終値がゼロ（取引がない）ときを除いて、データを配列に格納する。
for row in cur.fetchall():            
    time_array_outside.append(row[0]) 
    temperature_array_outside.append(row[1])
    pressure_local_array_outside.append(row[2])
    pressure_sea_array_outside.append(row[3])
    humidity_array_outside.append(row[4])
    
 
# plt.rcParams['font.family'] = 'Arial'
plt.rcParams["font.size"] = 28

fig, ax1 = plt.subplots(figsize=(20,13))
fig.autofmt_xdate()
formatter = mdates.DateFormatter("%H:%M")
ax1.xaxis.set_major_formatter(formatter)
span = pd.to_datetime([yesterday.strftime("%Y-%m-%d"), dt_now.strftime("%Y-%m-%d")])
ax1.scatter(time_array_workroom, temperature_array_workroom, s=60, c='k', marker='x', label='workroom')
ax1.scatter(time_array_outside, temperature_array_outside, s=60, c='r', marker='x', label='outside')
ax1.set_xlim(span)


ax1.set_title("Temperature history on " + yesterday.strftime("%Y-%m-%d"))
ax1.set_xlabel("time")
ax1.set_ylabel("temperature, degC")
ax1.grid()
ax1.minorticks_on()
ax1.spines["top"].set_linewidth(7)
ax1.spines["left"].set_linewidth(7)
ax1.spines["bottom"].set_linewidth(7)
ax1.spines["right"].set_linewidth(7)
ax1.tick_params(direction="in", width=7, length=15)
ax1.tick_params(which='minor', direction="in", width=4, length=10)
ax1.legend()

plt.savefig("/home/takuya/homeHK/temperature_graph/temperature_history_" + yesterday.strftime("%Y-%m-%d") + ".jpg")

cur.close
conn.close

line_notify_token = 'awxg8bTAUxDvfWPwaKZsUt1KQnWrGKAWlj8ypLeOCL6'
line_notify_api = 'https://notify-api.line.me/api/notify'
headers = {'Authorization': f'Bearer {line_notify_token}'}
data = {'message': f'\nTemperature history of home on ' + yesterday.strftime("%a %b %d, %Y")}
files = {"imageFile":open('/home/takuya/homeHK/temperature_graph/temperature_history_' + yesterday.strftime("%Y-%m-%d") + ".jpg", 'rb')}
requests.post(line_notify_api, headers = headers, params = data, files=files)
