import RPi.GPIO as GPIO
import datetime
import time
import MySQLdb

DOOR_KEY_PIN = 26

dt_now = datetime.datetime.now()

GPIO.setmode(GPIO.BCM)

GPIO.setup(DOOR_KEY_PIN, GPIO.IN)

key = GPIO.input(DOOR_KEY_PIN)
print(key)

GPIO.cleanup()

connection = MySQLdb.connect(
    host='localhost',
    user='homeHK',
    passwd='p8PYvkZiTsKm',
    db='homeHK')

cursor = connection.cursor()

cursor.execute("insert into door_key values(\'" + str(dt_now.strftime('%Y-%m-%d %H:%M:%S')) + "\', " + str(key) + ")")

connection.commit()

connection.close()
