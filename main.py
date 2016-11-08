import RPi.GPIO as GPIO
from time import sleep


# constants
WINDOW = 11  # GPIO port for the 'window' (a.k.a. alarm initiation)
ALARM = 13  # port for alarm(s)
LOGIN = 15  # port for button to initiate login protocol
LOGIN_PASS = 'jemoeder'  # password for login

alarmActivated = False

def detection(port):  # We start by checking, as fast as we can, for a button press to init alarm.
    while True:
        if GPIO.input(port):  # As soon as we have input, we break the while loop.
            break


def activateAlarm():
    time_per_step = 10

    GPIO.setwarnings(False)

    def incrementBrightness(maximum, offset):
        for looping in range(time_per_step):
            for x in range(maximum):
                GPIO.output(ALARM, x < offset)

    mymax = 100
    while not GPIO.input(LOGIN):
        for myOffset in range(mymax):
            incrementBrightness(mymax, myOffset)
        for myOffset in reversed(range(mymax)):
            incrementBrightness(mymax, myOffset)


def login():
    userPass = input('Typ het wachtwoord in om het alarm uit te zetten:')

def init():
    # initiating GPIO header
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(WINDOW, GPIO.IN)
    GPIO.setup(ALARM, GPIO.OUT)

    detection(WINDOW)
    activateAlarm()
    login()

