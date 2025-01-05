import qrcode

from lib.config import WIFI_SSID, WIFI_PASSWORD

# Generate the QR code for the WiFi connection



def create_qr_code():
   """Create a QR code for the WiFi connection."""
   wifi_config = f"WIFI:T:WPA;S:{WIFI_SSID};P:{WIFI_PASSWORD};;"
   qr = qrcode.QRCode(
      version=1,
      error_correction=qrcode.constants.ERROR_CORRECT_L,
      box_size=10,
      border=4,
   )
   qr.add_data(wifi_config)
   qr.make(fit=True)

   # Create an image from the QR Code instance
   img = qr.make_image(fill='black', back_color='white')

   # Save the image as a PNG file
   img.save("wifi_qr_code.png")
   print("QR code generated and saved as wifi_qr_code.png")


def main():
   create_qr_code()

if __name__ == "__main__":
   main()