import time

from lib.relay_controller import RelayController, relay
from lib.config import RELAY_IN_PIN


try:
   relay = RelayController(in_pin=RELAY_IN_PIN, active_low=False)

   for _ in range(5):
      relay.toggle()
      time.sleep(1)
      relay.toggle()
      time.sleep(0.2)

   relay.on()
   time.sleep(1)
   relay.off()

except Exception as e:
   print(e)