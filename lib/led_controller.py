# import neopixel
from machine import Pin
import lib.config as config

import time


class LedController():
   def __init__(self, pin):
      self.led = Pin(pin, Pin.OUT)
      self.is_on = False # LED State

   def on(self):
      self.led.on()
      self.is_on = True

   def off(self):
      self.led.off()
      self.is_on = False

   def toggle(self):
      if self.is_on:
         self.off()
      else:
         self.on()

   def set_state(self, state):
      """Set the LED state."""
      self.is_on = state
      self.led.value(1 if state else 0)

   def blink(self, duration_s, delay_s:int=0.5):
      for _ in range(int(duration_s/(delay_s*2))):
         self.on()
         time.sleep_ms(int(delay_s * 1000))
         self.off()
         time.sleep_ms(int(delay_s * 1000))




# class LedController():
#    def __init__(self, led_pin, rgb):
#       self.led_pin = led_pin
#       self.rgb = rgb
#       self.state = False
#       if self.rgb:
#          pass
#          # self.led = neopixel.NeoPixel(Pin(config.LED_PIN), 1, bpp=3)
#       else:
#         self.led =  Pin(config.LED_PIN, Pin.OUT)

#    def setup(self):
#       self.led.fill((0, 0, 0))
#       self.led.write()

#    def set_color(self, r, g, b):
#       self.led[0] = (r, g, b)
#       self.led.write()





# built_in_led = LedController(led_pin=config.LED_PIN, rgb=False)
led = Pin(config.LED_PIN, Pin.OUT)

led = LedController(config.LED_PIN)


