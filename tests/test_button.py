import time, sys
from machine import Pin
# from lib.button_handler import button  # Import the button object directly from the handler
# from lib.button_handler import button_presses
from lib.button_handler import ButtonHandler
from lib.led_controller import led  # Import the built-in LED object directly from the LED controller
import lib.config as config
# from tqdm import tqdm

button_handler = ButtonHandler(config.BUTTON_PIN)



# def print_flush(text):
#    sys.stdout.write(text + '\n')  # Use write to print directly to stdout
#    sys.stdout.write(sys.stdout.buffer)  # This forces immediate output on some setups

# Global counter for button presses
# button_presses = 0

# LED Setup (Pin setup for built-in LED or any external LED)
# led = Pin(config.LED_PIN, Pin.OUT)

# Test procedure to count button presses in 60 seconds
def test_button_press_within_60s():
   button_handler.button_presses = 0 # Reset button press count

   # Start time
   start_time = time.time()

   print(f"press the button now:")
   # Run test for 60 seconds, tracking button presses
   while time.time() - start_time < 20:
      if button_handler.get_button_presses() >= 8:  # If the button has been pressed 8 times, break the loop
         break
      time.sleep(0.1)  # Delay to reduce CPU usage during the test

   # with tqdm(total=60, desc="Press the button:", unit="sec") as pbar:
   #    while time.time() - start_time < 60:
   #       if button_presses >= 8:  # If the button has been pressed 8 times, break the loop
   #             break

   #       # Check for a button press (replace with your actual logic)

   #       pbar.update(0.1)  # Update progress bar every 0.1 seconds to simulate time passing
   #       time.sleep(0.1)  # Delay to reduce CPU usage

   # After 60 seconds, check if the button was pressed 8 times
   print(f"Button was pressed {button_handler.get_button_presses()} times in 60 seconds.")

   # Assertion (test validation)
   try:
      assert button_handler.get_button_presses() >= 8  # Ensure the button was pressed 8 times within 60 seconds
      print("Test passed successfully!")
   except AssertionError:
      print("Assertion Error: Button was not pressed enough times within 60 seconds.")

# Run the test
test_button_press_within_60s()
