from pygame import mixer
import random
import time
import keyboard
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
# from playsound import playsound


#            PRESS SPACE TO START
# ----- THE AI USES A MARKOV CHAIN AND      -----
# ----- HAND GESTURE DETECTION FOR MOVES.   -----


mixer.init()
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # width
cap.set(4, 480)
detector = HandDetector(maxHands=1)

# -----
global playerMove
global prev_play
global guessnum
global display

timer = 0
stateResult = False
startGame = False
scores = [0, 0]
display = ""
steps = {}
prev_play = ''
results = {"p1": 0, "ai": 0, "tie": 0}
opponent_history = []
steps = {}
guessnum = 1


def computer(prev_play, opponent_history=[]):
    global guessnum, guessnum
    global playerMove

    # prev_play = playerMove
    if prev_play != "":
        opponent_history.append(prev_play)
    num = 2
    history = opponent_history
    guess = 'S'
    guessnum = 3
    if len(history) > num:
        patterns = join(history[-num:])
        if join(history[-(num + 1):]) in steps.keys():
            steps[join(history[-(num + 1):])] += 1
        else:
            steps[join(history[-(num + 1):])] = 1
        possib = [patterns + 'R', patterns + 'P', patterns + 'S']
        # print(possib)
        for i in possib:
            if not i in steps.keys():
                steps[i] = 0  ###
        pred = max(possib, key=stepby)
        if pred[-1] == 'R':
            guess = 'P'
            guessnum = 2
        if pred[-1] == 'P':
            guess = 'S'
            guessnum = 3
        if pred[-1] == 'S':
            guess = 'R'
            guessnum = 1
    # print(guess)
    # print(guessnum)
    # print(opponent_history)


def stepby(key):
    return steps[key]


def join(moves):
    return "".join(moves)


def scoring():
    global display
    if (playerMove == 1 and guessnum == 3) or \
            (playerMove == 2 and guessnum == 1) or \
            (playerMove == 3 and guessnum == 2):
        scores[1] += 1
        results['p1'] += 1
        display = "You Won!"

    if (playerMove == 3 and guessnum == 1) or \
            (playerMove == 1 and guessnum == 2) or \
            (playerMove == 2 and guessnum == 3):
        scores[0] += 1
        results['ai'] += 1
        display = "A.I. Won!"

    if (playerMove == 1 and guessnum == 1) or \
            (playerMove == 2 and guessnum == 2) or \
            (playerMove == 3 and guessnum == 3):
        results['tie'] += 1
        display = "IT'S A TIE"


def gestures():
    global playerMove
    global prev_play
    if hands:
        playerMove = None
        hand = hands[0]
        fingers = detector.fingersUp(hand)

        if fingers == [0, 0, 0, 0, 0]:
            playerMove = 1  # rock
            prev_play = 'R'

        if fingers == [1, 1, 1, 1, 1]:
            playerMove = 2  # paper
            prev_play = 'P'

        if fingers == [0, 1, 1, 0, 0]:
            playerMove = 3  # scissors
            prev_play = 'S'


def stats():
    games_won = results['ai'] + results['p1']

    if games_won == 0:
        win_rate = 0
    else:
        win_rate = results['p1'] / games_won * 100

    print("result:", results)
    print(f"Human win rate: {win_rate}%")


# -----

while True:
    imgBG = cv2.imread("Stuff/BG.png")
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0, 0), None, 1.04, 1.04)
    imgScaled = imgScaled[:, 0:500]

    hands, img = detector.findHands(imgScaled)

    if startGame:

        if stateResult is False:
            timer = time.time() - initialTime

            # cv2.putText(imgBG, str(int(timer)), (970, 675), cv2.FONT_HERSHEY_SIMPLEX, 6, (230, 230, 250), 16)
            cv2.putText(imgBG, str("GO"), (940, 665), cv2.FONT_HERSHEY_SIMPLEX, 4, (230, 230, 250), 10)

            if timer > 1:
                stateResult = True
                timer = 0

                # pygame mixer
                sound = mixer.Sound('retro.mp3')
                sound.play()
                # Gesture Detection
                gestures()
                # Computer's move
                computer(prev_play, opponent_history)
                # Scoreboard
                scoring()
                # final stats
                stats()

                imgAI = cv2.imread(f'Stuff/{guessnum}.png', cv2.IMREAD_UNCHANGED)  # DISPLAY AI CHOICE
                imgBG = cvzone.overlayPNG(imgBG, imgAI, (295, 398))  # on img background

    imgBG[398:897, 1220:1720] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (295, 398))

    cv2.putText(imgBG, str(scores[0]), (690, 380), cv2.FONT_HERSHEY_SIMPLEX, 2, (230, 230, 250), 5)
    cv2.putText(imgBG, str(scores[1]), (1650, 380), cv2.FONT_HERSHEY_SIMPLEX, 2, (230, 230, 250), 5)
    cv2.putText(imgBG, str(display), (950, 500), cv2.FONT_HERSHEY_SIMPLEX, 1, (45, 45, 45), 6)

    # cv2.imshow("Image", img)
    cv2.imshow("RPS", imgBG)
    # cv2.imshow("stuff/rockcosmos.png", rock)
    # cv2.imshow("Scaled", imgScaled)

    key = cv2.waitKey(1)
    if keyboard.is_pressed('space'):
        startGame = True
        initialTime = time.time()
        stateResult = False
        display = ""
