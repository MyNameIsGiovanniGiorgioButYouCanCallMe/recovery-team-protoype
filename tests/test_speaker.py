import speaker_controller
import time

speaker_controller.setup()

while True:
   speaker_controller.play_tone(1000, 500)
   time.sleep(1)