from machine import PWM, Pin
import lib.config as config
import time

speaker = PWM(Pin(config.SPEAKER_PIN))

def setup():
   speaker.duty(0)

def play_tone(frequency, duration):
   speaker.freq(frequency)
   speaker.duty(512)
   time.sleep_ms(duration)
   speaker.duty(0)