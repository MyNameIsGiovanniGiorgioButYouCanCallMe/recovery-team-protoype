from machine import Pin
from lib.config import RELAY_IN_PIN

class RelayController:
   def __init__(self, in_pin:int, active_low:bool= False):
      # Pins:
      # self.COM = Pin(com_pin, Pin.OUT)
      self.IN  = Pin(in_pin, Pin.OUT)
      # self.VCC = Pin(vcc_pin, Pin.OUT)

      # Relay State
      self.is_on = False
      self.active_state = 0 if active_low else 1


      # Meta data:
      self.times_toggled = 0

      # Turn off relay
      self.off()

   def on(self):
      self.IN.value(self.active_state)

      self.times_toggled += 1
      self.is_on = True



   def off(self):
      self.IN.value(not self.active_state)

      self.times_toggled += 1
      self.is_on = False


   def toggle(self):
      if self.is_on:
         self.off()
      else:
         self.on()

   def set_state(self, is_on:bool):
      """Set the relay state."""
      self.is_on = is_on
      self.IN.value(self.active_state if is_on else not self.active_state)


relay = RelayController(in_pin=RELAY_IN_PIN, active_low=False)