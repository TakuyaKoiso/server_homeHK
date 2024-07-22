import requests
import RPi.GPIO as GPIO
import datetime
import time
import MySQLdb

door_key_sig = 26

def main():
    dt_now = datetime.datetime.now()
    send_line_notify('\nHouse unlocked.\n'+ dt_now.strftime('%a %b %d, %Y %H:%M:%S')+ ' JST')

    connection = MySQLdb.connect(
    host='localhost',
    user='homeHK',
    passwd='p8PYvkZiTsKm',
    db='homeHK')
    cursor = connection.cursor()
    cursor.execute("insert into door_key values(\'" + str(dt_now.strftime('%Y-%m-%d %H:%M:%S')) + "\', " + str(0) + ")")
    connection.commit()
    connection.close()

def send_line_notify(notification_message):
    line_notify_token = 'gAIzuxbAS7StJxMpSmGvW5DcrTzhcTPDklzATcz5P5m'
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {line_notify_token}'}
    data = {'message': f'{notification_message}'}
    requests.post(line_notify_api, headers = headers, data = data)

GPIO.setmode(GPIO.BCM)
GPIO.setup(door_key_sig, GPIO.IN)

while 1:
    door_key_status = GPIO.input(door_key_sig)
    if door_key_status == 0:
        main()
        time.sleep(60)

    time.sleep(5)
