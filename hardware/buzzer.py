import RPi.GPIO as GPIO
import time

# pin number for buzzer
BUZZER_PIN = 17

# passive buzzer
# BUZZER_PIN = 4

# class to control buzzer on/off
class BuzzerControl():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)
    
    def turn_on(self):
        try:
            GPIO.output(BUZZER_PIN,GPIO.HIGH)
            # passive buzzer use PWM to simulate Analog signal
            # buzz = GPIO.PWM(BUZZER_PIN, 440)
            # Buzz.start(50)
            return True
        except:
            print("Exception when setting Buzzer PIN to HIGH")
            return False
    
    def turn_off(self):
        try:
            GPIO.output(BUZZER_PIN,GPIO.LOW)
            return True
        except:
            print("Exception when setting BUzzer PIN to LOW")
            return False
    



