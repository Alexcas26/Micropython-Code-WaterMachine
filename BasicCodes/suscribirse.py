import time
#from mqtt import MQTTClient
from mqtt import MQTTClient_lib as MQTTClient
import machine
import micropython
import network
from network import WLAN
#import esp
#esp.osdebug(None)
import gc
gc.collect()

mqtt_server = '10.18.100.144'
#client_id = "2587fd2a-3538-4749-b78f-b565f83bbcba"

topic = b'sub'

def sub_cb(topic, msg):
  print(msg)

#station = network.WLAN(network.STA_IF)
station = network.WLAN(mode=network.WLAN.STA)
#station.scan()
station.connect(ssid='TALLER', auth=(WLAN.WPA2, 'pescadofrito'))

while station.isconnected() == False:
  pass

print('Connection successful')
#print(station.ifconfig())

client = MQTTClient("117225ea-e098-4f37-ae55-b735124f770c", mqtt_server, port=1883)
client.set_callback(sub_cb)
client.connect()
client.subscribe(topic)

while True:
    try:
        new_message = client.check_msg()     
    except OSError as e:
        restart_and_reconnect()