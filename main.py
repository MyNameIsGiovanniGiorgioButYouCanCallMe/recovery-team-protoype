from machine import Pin
# import config
import time

from lib.app import run

def main():
   print("Welcome to the Physio Ball!")
   time.sleep(0.1)
   run()
   time.sleep(0.1)


main()

if __name__ == '__main__':
   main()