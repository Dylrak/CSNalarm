import RPi.GPIO as GPIO

# constants
WINDOW_PORT = 11  # GPIO port for the 'window' (a.k.a. alarm initiation)
ALARM_PORT = 13  # port for alarm(s)
LOGIN_PORT = 15  # port for button to initiate login protocol
LOGIN_PASS = 'jemoeder'  # password for login


class State:
    IDLE = 0
    ALARM = 1
    LOGIN = 2


class Main:
    def __init__(self):
        # initiating GPIO header
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(WINDOW_PORT, GPIO.IN)
        GPIO.setup(ALARM_PORT, GPIO.OUT)
        GPIO.setup(LOGIN_PORT, GPIO.IN)
        state = State.IDLE
        self.running = True
        while self.running:  # MAIN while-loop, checks for program state.
            if state == State.IDLE:  # IDLE State means detecting if someone 'broke in'
                if GPIO.input(WINDOW_PORT):
                    state = State.ALARM
                    GPIO.output(ALARM_PORT, GPIO.HIGH)
            else:  # Else, the state is ALARM or LOGIN. This means we wait for login press to enter password.
                if GPIO.input(LOGIN_PORT):
                    state = State.LOGIN
                if state == State.LOGIN:
                    if not LOGIN_PASS == input('Voer uw wachtwoord in: '):
                        print('Uw wachtwoord klopt niet.')
                        while not LOGIN_PASS == input('Voer uw wachtwoord in: '):
                            print('Uw wachtwoord klopt niet.')
                        # After this while loop we have a valid password.
                        state = State.IDLE
                        GPIO.output(ALARM_PORT, False)
        GPIO.cleanup()
