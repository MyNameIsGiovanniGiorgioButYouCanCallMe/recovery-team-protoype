import network
import socket
from machine import Pin
from lib.config import WIFI_SSID, WIFI_PASSWORD, LED_PIN
from lib.led_controller import LedController

class WebServer:
   def __init__(self, ssid="ssid", password="test-123"):
      self.ssid = ssid
      self.password = password
      self.ip = None
      self.port = 80

      self.status_led = LedController(LED_PIN, rgb=False)

      self.is_heating_on = False
      self.is_button_on = False
      self.is_led_on = False

      self.is_server_on = False

      self.is_toggled = False

   def start_access_point(self):
      sta_if = network.WLAN(network.STA_IF)
      sta_if.active(False)

      ap = network.WLAN(network.AP_IF)
      ap.config(essid=self.ssid, password=self.password)
      ap.active(True)

      print("Creating Access Point...")
      while not ap.active():
         pass  # Wait for the AP to start

      self.ip = ap.ifconfig()[0]
      print(f"Access Point created. Connect to SSID: {self.ssid} with password: {self.password}")
      print(f"Access the web server at http://{self.ip}:{self.port}")



   def start_server(self):
      # Set up the socket
      addr = socket.getaddrinfo(self.ip, 80)[0][-1]
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.bind(addr)
      sock.listen(5)
      self.is_server_on = True
      print("Web server running. Waiting for connections...")
      try:
         while True:
            client, addr = sock.accept()
            print("Client connected from", addr)

            # Read HTTP request
            request = client.recv(1024)

            if request.startswith(b'GET') or request.startswith(b'POST'):
               try:
                  decoded_request = request.decode('utf-8')
                  print("Decoded request:", decoded_request)
               except UnicodeError:
                  print("Error decoding request")
                  decoded_request = ""
            else:
               print("Non-HTTP request received. Raw data:", request)
               decoded_request = ""

            print("Request:", request)

            # Handle requests
            if "GET /toggle" in decoded_request:
               self.is_button_on = not self.is_button_on
               # self.is_button_on.set_state(self.is_toggled)
               print("Toggle button pressed. New state:", self.is_toggled)

            ...

            # if '/toggle' in decoded_request:
            #    self.is_toggled = not self.is_toggled
            #    self.status_led.set_state(self.is_toggled)
            #    print("Toggle button pressed. New state:", self.is_toggled)
            # elif '/heating' in decoded_request:
            #    self.is_heating = not self.is_heating
            #    print("Heating button pressed. New state:", self.is_heating)
            # elif '/led' in decoded_request:
            #    self.is_led_on = not self.is_led_on
            #    self.status_led.set_state(self.is_led_on)
            #    print("LED button pressed. New state:", self.is_led_on)


            # Create an HTTP response
            html = self.generate_html()
            client.send("HTTP/1.1 200 OK\r\n")
            client.send("Content-Type: text/html\r\n")
            client.send("\r\n")
            client.sendall(html)
            client.close()

            if "exit" in decoded_request:
               print("Exit command received. Shutting down the server.")
               break
            if not self.is_server_on:
               print("Server is off.")
               break

      except KeyboardInterrupt:
         print("Keyboard interrupt received. Shutting down the server.")

      finally:
         print("Shutting down the server.")
         sock.close()


   @staticmethod
   def home_page():
      return b"""
      <!DOCTYPE html>
      <html>
      <head>
         <title>MicroPython Web Server</title>
      </head>
      <body>
         <h1>Hello from MicroPython!</h1>
         <p>You are connected to the device's private network.</p>
      </body>
      </html>
      """

   @staticmethod
   def generate_html(is_toggled=False, is_heating=False, is_led_on=False):
      """Generate the HTML content for the web page with three buttons."""
      toggle_state = "ON" if is_toggled else "OFF"
      heating_state = "ON" if is_heating else "OFF"
      led_state = "ON" if is_led_on else "OFF"
      toggle_color = "red" if is_toggled else "green"
      heating_color = "red" if is_heating else "green"
      led_color = "red" if is_led_on else "green"

      # color = {"ON": "green", "OFF": "red"}


      return f"""
      <!DOCTYPE html>
      <html>
      <head>
         <title>MicroPython Web Server</title>
         <style>
               body {{ font-family: Arial, sans-serif; text-align: center; padding: 20px; }}
               button {{ padding: 15px; margin: 10px; font-size: 16px; }}
               .status {{ font-weight: bold; margin-bottom: 10px; }}
         </style>
      </head>
      <body>
         <h1>Physio Ball Controll Panel</h1>
         <p>You are connected to the device's private network.</p>

         <div>
               <p class="status">Toggle State: <strong>{toggle_state}</strong></p>
               <button style="background-color; {toggle_color}color= white;" onclick="sendRequest('toggle')">Toggle</button>
         </div>

         <div>
               <p class="status">Heating State: <strong>{heating_state}</strong></p>
               <button style="background-color; {heating_color}color= white;" onclick="sendRequest('heating')">Toggle Heating</button>
         </div>

         <div>
               <p class="status">LED State: <strong>{led_state}</strong></p>
               <button style="background-color; {led_color}color= white;" onclick="sendRequest('led')">Toggle LED</button>
         </div>

         <script>
               function sendRequest(action) {{
                  fetch('/' + action)
                     .then(response => response.text())
                     .then(data => console.log(data))
                     .catch(error => console.error('Error:', error));
               }}
         </script>
      </body>
      </html>
      """.encode('utf-8')


def run():
   led = Pin(LED_PIN, Pin.OUT)


   # Configure the AP with an SSID and password
   ssid = WIFI_SSID
   password = WIFI_PASSWORD

   server = WebServer(ssid, password)
   led.on()

   server.start_access_point()
   server.start_server()
   led.off()


if __name__ == "__main__":
   run()