import RPi.GPIO as GPIO
import time
import random
import sqlite3

PORT_LAMP = 11
PORT_PLAYER1 = 13
PORT_PLAYER2 = 15

KEY_PLAY_GAME = 'S'
KEY_HIGHSCORE = 'H'
KEY_QUIT = 'A'

FILE_HIGHSCORES = 'highscores.db'

GPIO.setmode(GPIO.BOARD)

GPIO.setup(PORT_LAMP, GPIO.OUT)
GPIO.setup(PORT_PLAYER1, GPIO.IN)
GPIO.setup(PORT_PLAYER2, GPIO.IN)

connection = sqlite3.connect(FILE_HIGHSCORES)
cursor = connection.cursor()

initSQL = """
    CREATE TABLE IF NOT EXISTS scores
    (
        id INTEGER AUTO INCREMENT,
        score REAL NOT NULL,
        name TEXT NOT NULL
    )
"""

cursor.execute(initSQL)


def writeScoreToFile(name, score):
    _sql = "INSERT INTO scores (score, name) VALUES ('{}', {})".format(score, name)
    cursor.execute(_sql)

def retrieveHighscores():
    _string = ''
    _sql = "SELECT name, score FROM scores ORDER BY score DESC"
    cursor.execute(_sql)
    results = cursor.fetchall()
    print(results)
    for piece in results:
        _string += 'Name: {:10}, Score: {}\n'.format(piece[0], piece[1])
    return _string

mainloop = True
while mainloop:
    userInput = input('wat wilt u doen?\nnog een [{}] spel spelen\nde [{}] highscores zien\n[{}] afsluiten'.format(KEY_PLAY_GAME, KEY_HIGHSCORE, KEY_QUIT)).upper()
    if userInput == KEY_PLAY_GAME:
        # Wait for a random peiod of time
        time.sleep(random.randint(4, 9))

        # light the LED
        GPIO.output(PORT_LAMP, True)
        # start timing
        timeStart = time.time()
        # wait until either player A or player B presses the button
        playerA, playerB = GPIO.input(PORT_PLAYER1), GPIO.input(PORT_PLAYER2)
        while not (playerA or playerB):
            time.sleep(0.001)
            playerA, playerB = GPIO.input(PORT_PLAYER1), GPIO.input(PORT_PLAYER2)

        # stop timing
        timeEnd = time.time()
        # put the lamp out
        GPIO.output(PORT_LAMP, False)

        # announce the victor
        winner = 'A' if playerA else 'B'
        timeDelta = timeEnd-timeStart

        print('Player {} won with a reaction time of {}'.format(winner, timeDelta))

        localUserInput = input('Enter your name for the highscores!')
        writeScoreToFile(localUserInput, timeDelta)
    elif userInput == KEY_HIGHSCORE:
        print(retrieveHighscores())
        input('Press a key to continue')

    elif userInput == KEY_QUIT:
        # Quit the game - kill the mainloop
        mainloop = False

    else:
        time.sleep(1)
        continue

#end of loop
connection.commit()
connection.close()
GPIO.cleanup()
