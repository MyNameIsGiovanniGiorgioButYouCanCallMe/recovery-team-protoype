from machine import Pin
import config

relay = Pin(config.RELAY_PIN, Pin.OUT)

def setup():
   relay.off()

def toggle(state):
   relay.value(state)