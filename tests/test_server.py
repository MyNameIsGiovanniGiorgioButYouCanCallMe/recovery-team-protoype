import network
import socket
from lib.config import WIFI_SSID, WIFI_PASSWORD, LED_PIN
from machine import Pin


class TestWebServer:
    def __init__(self, ssid="TestAP", password="12345678"):
        self.ssid = ssid
        self.password = password
        self.ip = None
        self.port = 80
        self.test_completed = False

    def start_access_point(self):
         sta_if = network.WLAN(network.STA_IF)
         sta_if.active(False)

         ap = network.WLAN(network.AP_IF)
         ap.config(essid=self.ssid, password=self.password)
         ap.active(True)

         print("Creating Access Point...")
         while not ap.active():
               pass  # Wait for the AP to start
         print("Access Point created.")


         self.ip = ap.ifconfig()[0]
         print(f"Access Point created. Connect to SSID: {self.ssid} with password: {self.password}")
         print(f"Access the server at http://{self.ip}:{self.port}")

    def start_server(self):
        # Set up the socket
        addr = socket.getaddrinfo(self.ip, self.port)[0][-1]
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(addr)
        sock.listen(5)
      #   sock.settimeout(10)  # Set timeout for accepting a connection
        print("Web server running. Waiting for 'test_completed' message...")

        while not self.test_completed:
            print("Waiting for a client connection...")
            client, addr = sock.accept()
            print("Client connected from", addr)

            # Read HTTP request

            request = client.recv(1024)
            # Check if the received data contains valid HTTP headers
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

            # request = client.recv(1024).decode('utf-8')
            print("Request:", request)

            # Check for the "test_completed" message
            if "test_completed" in request:
                print("Test completed message received.")
                self.test_completed = True
                response = self.generate_html("Test passed! Thank you!")
            else:
                response = self.generate_html("Waiting for 'test_completed' message...")

            # Send response
            client.send("HTTP/1.1 200 OK\r\n")
            client.send("Content-Type: text/html\r\n")
            client.send("\r\n")
            client.sendall(response)
            client.close()

        print("Shutting down the server.")
        sock.close()

    @staticmethod
    def generate_html(message):
        """Generate HTML content for the web page."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Physio Ball</title>
        </head>
        <body>
            <h1>{message}</h1>
        </body>
        </html>
        """.encode('utf-8')

def run():
   led = Pin(LED_PIN, Pin.OUT)
   # Configure the AP with an SSID and password
   server = TestWebServer(WIFI_SSID, WIFI_PASSWORD)
   server.test_completed = False

   led.on()
   server.start_access_point()
   server.start_server()
   led.off()



run()