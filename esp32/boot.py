from machine import Pin
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

ssid = ''
password = ''
mqtt_server = ''  #Replace with your MQTT Broker IP

client_id = ubinascii.hexlify(machine.unique_id())
topic_pub = b'DISPLACEMENT'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())