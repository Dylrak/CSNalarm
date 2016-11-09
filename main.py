import RPi.GPIO as GPIO
import sys
import select
from time import sleep


# constants
WINDOW_PORT = 11  # GPIO port for the 'window' (a.k.a. alarm initiation)
ALARM_PORT = 13  # port for alarm(s)
LOGIN_PORT = 15  # port for button to initiate login protocol
LOGIN_PASS = 'jemoeder'  # password for login


class State:
    IDLE = 0
    ALARM = 1
    LOGIN = 2
    # These last two states are for the alarms.
    INCREASING = 3
    DECREASING = 4


class Main:
    def __init__(self):
        # initiating GPIO header
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(WINDOW_PORT, GPIO.IN)
        GPIO.setup(ALARM_PORT, GPIO.OUT)
        state = State.IDLE
        alarm = Alarm()
        while True:  # MAIN while-loop, checks for program state.
            if state == State.IDLE:  # IDLE State means detecting if someone 'broke in'
                if GPIO.input(WINDOW_PORT):
                    state = State.ALARM
            else:  # Else, the state is ALARM or LOGIN.
                alarm.changeBrightness()
                if state == State.LOGIN:
                    userHasEnteredPass, o, e = select.select([sys.stdin], [], [], 10)
                    if userHasEnteredPass and LOGIN_PASS == sys.stdin.readline().strip():  # sys.stdin is the user input
                        state = State.IDLE


class Alarm:

    def __init__(self):
        GPIO.setwarnings(False)
        self.brightness = 0
        self.state = State.INCREASING

    def changeBrightness(self):
        step = 10
        maximum = 100
        if self.state == State.INCREASING:
            self.brightness += step
            if self.brightness == maximum:
                self.state = State.DECREASING
        else:
            self.brightness -= step
            if self.brightness == 0:
                self.state = State.INCREASING
        GPIO.output(ALARM_PORT, self.brightness)
Main()
