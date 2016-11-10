import RPi.GPIO as GPIO
import threading
import time

# constants
WINDOW_PORT = 11  # GPIO port for the 'window' (a.k.a. alarm initiation)
ALARM_PORT = 13  # port for alarm(s)
LOGIN_PORT = 15  # port for button to initiate login protocol
LOGIN_PASS = 'jemoeder'  # password for login

TIME_PER_STEP = 10
MAX_STEPS = 100

class State:
    IDLE = 0
    ALARM = 1
    LOGIN = 2


# initiating GPIO header
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(WINDOW_PORT, GPIO.IN)
GPIO.setup(ALARM_PORT, GPIO.OUT)
GPIO.setup(LOGIN_PORT, GPIO.IN)
state = State.IDLE

isFlashing = False

running = True

def flashFunction(maxRange, offset):
    for looping in range(TIME_PER_STEP):
        for x in range(maxRange):
            GPIO.output(ALARM_PORT, x < offset)
            time.sleep(0.005)

while not GPIO.input(WINDOW_PORT):
    for offset in range(MAX_STEPS):
        flashFunction(MAX_STEPS, offset)
    for offset in reversed(range(MAX_STEPS)):
        flashFunction(MAX_STEPS, offset)


def flashing():
    """Thread flashing function"""
    while True:
        while isFlashing:
            for offset in range(MAX_STEPS):
                flashFunction(MAX_STEPS, offset)
            for offset in reversed(range(MAX_STEPS)):
                flashFunction(MAX_STEPS, offset)
        time.sleep(0.05)

flash_thread = threading.Thread(target=flashing)
flash_thread.start()

try:
    while running:  # MAIN while-loop, checks for program state.
        if state == State.IDLE:  # IDLE State means detecting if someone 'broke in'
            if GPIO.input(WINDOW_PORT):
                state = State.ALARM
                GPIO.output(ALARM_PORT, True)
                isFlashing = True
                # TODO: time the last time we switched the alarm on, call it timeSinceLastSwitch
                # TODO: compare timeSinceLastSwitch to currTime, if greater than set e.g. 1 second switch light on/off
        # Else, the state is ALARM or LOGIN. This means we wait for login press to enter password.
        elif GPIO.input(LOGIN_PORT):
           state = State.LOGIN
        elif state == State.LOGIN:
            if not LOGIN_PASS == input('Voer uw wachtwoord in: '):
                print('Uw wachtwoord klopt niet.')
                while not LOGIN_PASS == input('Voer uw wachtwoord in: '):
                    print('Uw wachtwoord klopt niet.')
            # After this while loop we have a valid password.
            state = State.IDLE
            isFlashing = False
finally:
    GPIO.cleanup()

