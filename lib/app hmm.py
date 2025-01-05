import network
import socket
import json
from machine import Pin, Timer
from lib.config import WIFI_SSID, WIFI_PASSWORD, LED_PIN, BUTTON_PIN, RELAY_IN_PIN
from lib.led_controller import LedController
from lib.relay_controller import RelayController
from lib.button_handler import ButtonHandler



class WebServer:
   def __init__(self, ssid="ssid", password="test-123"):
      self.ssid = ssid
      self.password = password
      self.ip = None
      self.port = 80


      self.relay = RelayController(in_pin=RELAY_IN_PIN, active_low=False)
      self.status_led = LedController(LED_PIN)
      self.button = ButtonHandler(BUTTON_PIN)

      self.is_heating_on = False
      self.is_button_on = False
      self.is_led_on = False

      self.is_server_on = False

      self.is_toggled = False
      # self.button_handler = ButtonHandler(pin=5)  # Physical button on pin 5

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
            if not request:
               print("Empty request received.")
               continue

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
               print("Toggle button pressed. New state:", self.is_button_on)

            if "GET /heating" in decoded_request:
               self.is_heating_on = not self.is_heating_on
               print("Heating button pressed. New state:", self.is_heating_on)

            if "GET /led" in decoded_request:
               self.is_led_on = not self.is_led_on
               self.status_led.set_state(self.is_led_on)
               print("LED button pressed. New state:", self.is_led_on)

            response = {
               "button_state": self.is_button_on,
               "heating_state": self.is_heating_on,
               "led_state": self.is_led_on
            }


            if "exit" in decoded_request:
               print("Exit command received. Shutting down the server.")
               break

            # Check if the physical button was pressed and toggle
            if self.button_handler.has_been_pressed():
                self.is_button_on = not self.is_button_on
                print("Physical button pressed. New state:", self.is_button_on)
                response["button_state"] = self.is_button_on

            # Return response to client as JSON

            client.send("HTTP/1.1 200 OK\r\n")
            client.send("Content-Type: application/json\r\n")
            client.send("\r\n")
            client.sendall(str(response).encode())
            client.close()


            html = self.generate_html(is_button_on=self.is_button_on, is_heating_on=self.is_heating_on, is_led_on=self.is_led_on)
            client.send("HTTP/1.1 200 OK\r\n")
            client.send("Content-Type: text/html\r\n")
            client.send("\r\n")
            client.sendall(html)
            client.close()


      except KeyboardInterrupt:
         print("Keyboard interrupt received. Shutting down the server.")

      except OSError as e:
         print(f"OSError occurred: {e}")
         client.close()

      finally:
         print("Shutting down the server.")
         sock.close()

   @staticmethod
   def generate_html(is_button_on=False, is_heating_on=False, is_led_on=False):
      """Generate the HTML content for the web page with three buttons."""
      button_state = "ON" if is_button_on else "OFF"
      heating_state = "ON" if is_heating_on else "OFF"
      led_state = "ON" if is_led_on else "OFF"
      button_color = "green" if is_button_on else "red"
      heating_color = "green" if is_heating_on else "red"
      led_color = "green" if is_led_on else "red"

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
         <h1>Physio Ball Control Panel</h1>
         <p>You are connected to the device's private network.</p>

         <div>
           <p class="status">Button State: <strong id="button-state">{button_state}</strong></p>
           <button id="button-btn" style="background-color: {button_color}; color: white;" onclick="sendRequest('button')">Toggle Button</button>
         </div>

         <div>
            <p class="status">Heating State: <strong id="heating-state">{heating_state}</strong></p>
            <button id="heating-btn" style="background-color: {heating_color}; color: white;" onclick="sendRequest('heating')">Toggle Heating</button>
         </div>

         <div>
            <p class="status">LED State: <strong id="led-state">{led_state}</strong></p>
            <button id="led-btn" style="background-color: {led_color}; color: white;" onclick="sendRequest('led')">Toggle LED</button>
         </div>

         <script>
           // Update the button colors and states dynamically when the page loads
           window.onload = function() {{
               updateButtonState();
           }};

           function updateButtonState() {{
               // Ensure initial state is reflected in the button colors
               let buttonState = document.getElementById('button-state').textContent;
               let buttonColor = buttonState === 'ON' ? 'red' : 'green';
               document.getElementById('button-btn').style.backgroundColor = buttonColor;
           }}

           function sendRequest(action) {{
               fetch('/' + action)
                   .then(response => response.json())
                   .then(data => {{
                       // Update the button colors and states dynamically
                       if (action === 'button') {{
                           document.getElementById('button-state').textContent = data.button_state ? 'ON' : 'OFF';
                           document.getElementById('button-btn').style.backgroundColor = data.button_state ? 'red' : 'green';
                       }} else if (action === 'heating') {{
                           document.getElementById('heating-state').textContent = data.heating_state ? 'ON' : 'OFF';
                           document.getElementById('heating-btn').style.backgroundColor = data.heating_state ? 'red' : 'green';
                       }} else if (action === 'led') {{
                           document.getElementById('led-state').textContent = data.led_state ? 'ON' : 'OFF';
                           document.getElementById('led-btn').style.backgroundColor = data.led_state ? 'red' : 'green';
                       }}
                   }})
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
