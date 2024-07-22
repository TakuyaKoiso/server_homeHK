#!usr/bin/env python
#使用例: # -*- coding: utf_8 -*-

import paho.mqtt.client as mqtt
import sys
import MySQLdb
import datetime

# ブローカーに接続できたときの処理
def on_connect(client, userdata, flag, rc):
  print("Connected with result code " + str(rc))  # 接続できた旨表示
  client.subscribe("BME680_workroom")  # subするトピックを設定 

# ブローカーが切断したときの処理
def on_disconnect(client, userdata, rc):
  if  rc != 0:
    print("Unexpected disconnection.")

# メッセージが届いたときの処理
def on_message(client, userdata, msg):
  # msg.topicにトピック名が，msg.payloadに届いたデータ本体が入っている
  mqtt_data = msg.payload.decode('utf8').split(', ')
  humidity = float(mqtt_data[0])
  pressure = float(mqtt_data[1])
  temperature = float(mqtt_data[2])
  pressure_sea = pressure*(1-(0.0065*115.3)/(temperature+0.0065*115.3+273.15))**-5.257
  
  connection = MySQLdb.connect(
    host='localhost',
    user='root',
    passwd='navier0928miwa',
    db='homeHK')
  
  dt_now = datetime.datetime.now()

  cursor = connection.cursor()
  cursor.execute("insert into BME680_workroom values(\'" + str(dt_now.strftime('%Y-%m-%d %H:%M:%S')) + "\', " + str(temperature) + ", " + str(pressure) + ", " + str(pressure_sea) + "," + str(humidity) + ", NULL)")

  connection.commit()
  connection.close()
  
  print(humidity)
  print(pressure)
  print(pressure_sea)
  print(temperature)
  sys.exit()

# MQTTの接続設定
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "takuya")                 # クラスのインスタンス(実体)の作成
client.on_connect = on_connect         # 接続時のコールバック関数を登録
client.on_disconnect = on_disconnect   # 切断時のコールバックを登録
client.on_message = on_message         # メッセージ到着時のコールバック
 
client.connect("localhost", 1883, 60)  # 接続先は自分自身
 
client.loop_forever()                  # 永久ループして待ち続ける