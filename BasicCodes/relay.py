# main.py -- put your code here!
from machine import Pin
from time import sleep
relay = Pin('P5', mode=Pin.OUT)

while True:
  relay.value(0)
  sleep(10)
  # RELAY OFF
  relay.value(1)
  sleep(10)