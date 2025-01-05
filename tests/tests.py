# ALL TESTS
print("Running all tests".upper())

try:
   from tests.test_leds import test_led_blink
   test_led_blink()
except Exception as e:
   print("LED test failed with exception: ".upper(), e)

try:
   from tests.test_button import test_button_press_within_60s
   test_button_press_within_60s()
except Exception as e:
   print("Button test failed with exception: ".upper(), e)
