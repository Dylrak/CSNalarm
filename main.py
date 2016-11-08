import RPi.GPIO as GPIO


# constants
WINDOW = 11  # GPIO port for the 'window' (a.k.a. alarm initiation)

# init
GPIO.setmode(GPIO.BOARD)
GPIO.setup(WINDOW, GPIO.IN)
while True:
    if GPIO.input(WINDOW) == 1:
        print('Button clicked!')
        break
