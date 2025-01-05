import network
import lib.config as config

def connect_to_wifi():
   wlan = network.WLAN(network.STA_IF)
   wlan.active(True)
   wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
   while not wlan.isconnected():
      pass