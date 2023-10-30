import RPi.GPIO as GPIO
import time

# pin number for LED
LED_PIN = 18

# class to control LED on/off
class LEDControl():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
    
    def turn_on(self):
        try:
            GPIO.output(LED_PIN,GPIO.HIGH)
            return True
        except:
            print("Exception when setting LED PIN to HIGH")
            return False
    
    def turn_off(self):
        try:
            GPIO.output(LED_PIN,GPIO.LOW)
            return True
        except:
            print("Exception when setting LED PIN to LOW")
            return False
    