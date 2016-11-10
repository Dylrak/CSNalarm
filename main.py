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

isflashing = False

running = True

def flashing():
    """Thread flashing function"""
        
    while True:
        if isflashing:
            GPIO.output(ALARM_PORT, True)
            time.sleep(0.1)
            GPIO.output(ALARM_PORT, False)
            time.sleep(0.1)
        time.sleep(0.25)


print('starting')
flash_thread = threading.Thread(target=flashing)

print('other program')
running = True
flash_thread.start()
while running:  # MAIN while-loop, checks for program state.
    if state == State.IDLE and GPIO.input(WINDOW_PORT):  # IDLE State means detecting if someone 'broke in'
        state = State.ALARM
        GPIO.output(ALARM_PORT, True)
        isflashing = True
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
        isflashing = False
        GPIO.output(ALARM_PORT, False)
    time.sleep(0.1)
print('starting threads')

GPIO.cleanup()
