import pandas as pd
import numpy as np
import MySQLdb
import pandas_datareader.data as pdr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import requests

dt_now = datetime.now() +timedelta(1)
yesterday = dt_now - timedelta(1)

conn = MySQLdb.connect(user='root', password='navier0928miwa', host='localhost', database='homeHK')
cur = conn.cursor()
cur.execute("select * from BME680_workroom where date_format(date_and_time,'%Y-%m-%d') = \"" + yesterday.strftime("%Y-%m-%d") + "\" order by date_and_time asc;")

time_array  = []
temperature_array = []

#終値がゼロ（取引がない）ときを除いて、データを配列に格納する。
for row in cur.fetchall():            
    time_array.append(row[0]) 
    temperature_array.append(row[1])
 
# plt.rcParams['font.family'] = 'Arial'
plt.rcParams["font.size"] = 28

fig, ax = plt.subplots(figsize=(20,13))
fig.autofmt_xdate()
formatter = mdates.DateFormatter("%H:%M")
ax.xaxis.set_major_formatter(formatter)
span = pd.to_datetime([yesterday.strftime("%Y-%m-%d"), dt_now.strftime("%Y-%m-%d")])
ax.plot(time_array, temperature_array, 'k', lw=3)
ax.set_xlim(span)

ax.set_title(yesterday.strftime("%Y-%m-%d"))
ax.set_xlabel("time")
ax.set_ylabel("temperature, degC")
ax.grid()
ax.minorticks_on()
ax.spines["top"].set_linewidth(7)
ax.spines["left"].set_linewidth(7)
ax.spines["bottom"].set_linewidth(7)
ax.spines["right"].set_linewidth(7)
ax.tick_params(direction="in", width=7, length=15)
ax.tick_params(which='minor', direction="in", width=4, length=10)
plt.savefig("/home/takuya/homeHK/temperature_graph/" + yesterday.strftime("%Y-%m-%d") + ".jpg")

cur.close
conn.close

line_notify_token = 'awxg8bTAUxDvfWPwaKZsUt1KQnWrGKAWlj8ypLeOCL6'
line_notify_api = 'https://notify-api.line.me/api/notify'
headers = {'Authorization': f'Bearer {line_notify_token}'}
data = {'message': f'\nTemperature history on ' + yesterday.strftime("%a %b %d, %Y")}
files = {"imageFile":open('/home/takuya/homeHK/temperature_graph/' + yesterday.strftime("%Y-%m-%d") + ".jpg", 'rb')}
requests.post(line_notify_api, headers = headers, params = data, files=files)
