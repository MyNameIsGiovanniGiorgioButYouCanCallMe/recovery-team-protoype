import config
import wifi_manager
import relay_controller
import led_controller
import button_handler
import speaker_controller

wifi_manager.connect_to_wifi()
relay_controller.setup()
led_controller.setup()
button_handler.setup()
speaker_controller.setup()

while True:
    if button_handler.is_button_pressed():
        relay_controller.toggle(True)
        led_controller.set_color(255, 0, 0)  # Red
        speaker_controller.play_tone(1000, 500)
    else:
        relay_controller.toggle(False)
        led_controller.set_color(0, 255, 0)  # Green
