import RPi.GPIO as GPIO

# constants
WINDOW = 11  # GPIO port for the 'window' (a.k.a. alarm initiation)
BREAK = 13
LED_GREEN = 15

# init
GPIO.setmode(GPIO.BOARD)

#GPIO WINDOW als input definieeren
GPIO.setup(WINDOW, GPIO.IN)
GPIO.setup(BREAK, GPIO.IN)

#GPIO LED_GREEN als output opzetten
GPIO.setup(LED_GREEN, GPIO.OUT)

time_per_step = 10

GPIO.setwarnings(False)


def myFunction(mymax, offset):
    for looping in range(time_per_step):
        for x in range(mymax):
            GPIO.output(LED_GREEN, x<offset)


mymax = 100
while not GPIO.input(WINDOW):
    for offset in range(mymax):
        myFunction(mymax, offset)
    for offset in reversed(range(mymax)):
        myFunction(mymax, offset)


            
