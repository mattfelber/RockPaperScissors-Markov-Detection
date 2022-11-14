from pygame import mixer
import random
import time
import keyboard
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector

# from playsound import playsound


# PRESS SPACE TO START.
# THE A.I. USES A MARKOV CHAIN AND HAND GESTURE DETECTION FOR MOVING.

mixer.init()

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # width
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0]
display = ""
steps = {}

global randomNumber
global prev_play


opponent_history = []
steps = {}
guessnum = 1
def player(prev_play, opponent_history=[]):
    global randomNumber, guessnum
    global playerMove

    #prev_play = playerMove
    if prev_play != "":
        opponent_history.append(prev_play)
    num = 3
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
        for i in possib:
            if not i in steps.keys():
                steps[i] = 0               ###
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
    print(guess)
    print(guessnum)
    randomNumber = guessnum

    return guess

def stepby(key):
   return steps[key]

def join(moves):
    return "".join(moves)

###########

while True:
    global playerMove

    imgBG = cv2.imread("Stuff/BG.png")
    success, img = cap.read()

    ###
    imgScaled = cv2.resize(img, (0, 0), None, 1.04, 1.04)
    imgScaled = imgScaled[:, 0:500]
    ###
    hands, img = detector.findHands(imgScaled)

    if startGame:

        if stateResult is False:
            timer = time.time() - initialTime
            # cv2.putText(imgBG, str(int(timer)), (970, 675), cv2.FONT_HERSHEY_SIMPLEX, 6, (230, 230, 250), 16)
            cv2.putText(imgBG, str("GO"), (940, 665), cv2.FONT_HERSHEY_SIMPLEX, 4, (230, 230, 250), 10)

            if timer > 1:
                stateResult = True
                timer = 0
                # for playing note.mp3 file
                # playsound('retro.mp3')      Playsound slowed down opencv try pygame mixer:
                sound = mixer.Sound('retro.mp3')
                sound.play()

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

                    # print(playerMove)
                    player(prev_play, opponent_history)
                    print(opponent_history)
                    # randomNumber = random.randint(1, 3)

                    imgAI = cv2.imread(f'Stuff/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (295, 398))

                    # player score
                    if (playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1
                        display = "You Won!"
                    # computer score
                    if (playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1
                        display = "A.I. Won!"
                    if (playerMove == 1 and randomNumber == 1) or \
                            (playerMove == 2 and randomNumber == 2) or \
                            (playerMove == 3 and randomNumber == 3):
                        display = "IT'S A TIE"

                    # print(playerMove)

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
