#!usr/bin/env python
#使用例: # -*- coding: utf_8 -*-

import paho.mqtt.client as mqtt
import sys
import MySQLdb
import datetime
import time
import requests

# ブローカーに接続できたときの処理
def on_connect(client, userdata, flag, rc):
  print("Connected with result code " + str(rc))  # 接続できた旨表示
  client.subscribe("door_key")  # subするトピックを設定 

# ブローカーが切断したときの処理
def on_disconnect(client, userdata, rc):
  if  rc != 0:
    print("Unexpected disconnection.")

# メッセージが届いたときの処理
def on_message(client, userdata, msg):
  # msg.topicにトピック名が，msg.payloadに届いたデータ本体が入っている
  mqtt_data = msg.payload.decode('utf8')
  
  if mqtt_data=="door_key_open":
    dt_now = datetime.datetime.now()
    send_line_notify('\n\nHouse unlocked.\n'+ dt_now.strftime('%a %b %d, %Y %H:%M:%S')+ ' JST')
    
  if mqtt_data=="door_key_close":
    dt_now = datetime.datetime.now()
    send_line_notify('\n\nHouse locked.\n'+ dt_now.strftime('%a %b %d, %Y %H:%M:%S')+ ' JST')
  
def send_line_notify(notification_message):
  line_notify_token = 'gAIzuxbAS7StJxMpSmGvW5DcrTzhcTPDklzATcz5P5m'
  line_notify_api = 'https://notify-api.line.me/api/notify'
  headers = {'Authorization': f'Bearer {line_notify_token}'}
  data = {'message': f'message: {notification_message}'}
  requests.post(line_notify_api, headers = headers, data = data)
#   sys.exit()

# MQTTの接続設定
client = mqtt.Client("door_key_line")                 # クラスのインスタンス(実体)の作成
client.on_connect = on_connect         # 接続時のコールバック関数を登録
client.on_disconnect = on_disconnect   # 切断時のコールバックを登録
client.on_message = on_message         # メッセージ到着時のコールバック
client.connect("localhost")  # 接続先は自分自身
 
client.loop_forever()                # 永久ループして待ち続ける