from machine import I2C
from machine import Pin
from machine import sleep

import time


# MPU6050
import mpu6050
i2c = I2C(scl=Pin(22), sda=Pin(21))     #initializing the I2C method for ESP32
mpu= mpu6050.accel(i2c)

def connect():
  print('Connecting to MQTT Broker...')
  global client_id, mqtt_server
  client = MQTTClient(client_id, mqtt_server, keepalive=60)
  client.connect()
  print('Connected to %s MQTT broker' % (mqtt_server))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
      start_time = time.time()
      AcX, AcY, AcZ = mpu.get_values()['AcX'], mpu.get_values()['AcY'], mpu.get_values()['AcZ']
      
      msg = str((AcX, AcY, AcZ))
      #msg = str(mpu.get_values())
      client.publish(b'DISPLACEMENT', msg)
      print('Publishing message: %s on topic %s' % (msg, topic_pub))
      end_time = time.time()
      delta_time = end_time - start_time
      print(delta_time)
      time.sleep(1-delta_time//1000)
  except OSError as e:
    restart_and_reconnect()