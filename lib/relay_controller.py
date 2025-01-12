from machine import Pin
# from lib.config import RELAY_IN_PIN

from machine import Pin

class RelayController:
   def __init__(self, in_pin:int, active_low:bool):
      # Initialize the pin as an output
      self.IN  = Pin(in_pin, Pin.OUT)

      # Relay State
      self.is_on = False
      self.active_state = 0 if active_low else 1

      # Meta data
      self.times_toggled = 0

      # Initially turn off the relay
      self.off()

   def off(self):
      """Turn the relay on by setting the pin to the active state."""
      if self.active_state == 0:
         self.IN.init(Pin.IN)
      else:
         # Turn it on (power up)
         self.IN.init(Pin.OUT)
         self.IN.value(self.active_state)

      self.times_toggled += 1
      self.is_on = True

   def on(self):
      """Turn the relay off by disabling the pin (set as input)."""
      if self.active_state == 0:
         self.IN.init(Pin.OUT)
         self.IN.value(self.active_state)
      else:
         # Turn it off (power down)
         self.IN.init(Pin.IN)  # Disable pin by setting it as input (high impedance state)
         # self.IN.value(not self.active_state) # optional


      self.times_toggled += 1
      self.is_on = False

   def toggle(self):
      """Toggle the relay state."""
      if self.is_on:
         self.off()
      else:
         self.on()

   def set_state(self, is_on:bool):
      """Set the relay state."""
      self.is_on = is_on
      if is_on:
         self.on()
      elif not is_on:
         self.off()

# relay = RelayController(in_pin=RELAY_IN_PIN, active_low=True)