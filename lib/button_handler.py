from machine import Pin
import lib.config as config
import time

# Debounce control
last_press = time.ticks_ms()  # Initialize the last press time
debounce_time = 300  # Time in milliseconds for debounce

# Number of valid button presses

button_presses = 100

def button_handler(pin):
   global last_press, button_presses
   current_time = time.ticks_ms()
   if time.ticks_diff(current_time, last_press) > debounce_time:
      button_presses += 1
      print(f"Button pressed for the {button_presses}. time!")
      last_press = current_time  # Update the last press time


button = Pin(config.BUTTON_PIN, Pin.IN, Pin.PULL_UP)

button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)


# while True:
#    print(f"Button has been pressed {button_presses} times.")
#    time.sleep(10)  # Sleep to reduce CPU usage


class ButtonHandler:
   def __init__(self, pin):
      self.button_presses = 0
      self.last_press = time.ticks_ms()
      self.debounce_time = 300  # Time in milliseconds for debounce
      self.button = Pin(pin, Pin.IN, Pin.PULL_UP)
      self.button.irq(trigger=Pin.IRQ_FALLING, handler=self.button_handler)

   def button_handler(self, pin):
      current_time = time.ticks_ms()

      if time.ticks_diff(current_time, self.last_press) > self.debounce_time:
         self.button_presses += 1  # Increment press count
         print(f"Button pressed for the {self.button_presses} time(s)!")
         self.last_press = current_time  # Update the last press time

   def get_button_presses(self):
      return self.button_presses