import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(0, GPIO.IN)
while True:
    if GPIO.input(0) == 1:
        print('Button clicked!')
        break
