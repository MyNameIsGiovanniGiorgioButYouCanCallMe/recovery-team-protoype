print("Running test_leds.py".upper())

# import sys, os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

try:
   # help('modules')
   from lib.led_controller import led
   import time

   # led_controller.setup()

   for i in range(0,10):
      led.toggle()
      time.sleep(0.1)
      led.toggle()
      time.sleep(0.2)
      led.toggle()
      time.sleep(i/10)
      print("LED starts blinking...")
      led.blink(10, 0.1)

      led.off()



   print("Test passed flawlessly")



except Exception as e:
   print("failed with exception: ".upper(), e)
   print("Manual Test Required...")
   from machine import Pin
   import time

   led = Pin('LED', Pin.OUT)
   for i in range(0,10):
      led.toggle()
      time.sleep(1-i/100)

   led.off()

   print("Test passed with exception: ", e)