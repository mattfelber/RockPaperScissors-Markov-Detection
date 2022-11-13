import random
import time
import keyboard
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # width
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0]
display = ""


while True:
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
            cv2.putText(imgBG, str(int(timer)), (970, 675), cv2.FONT_HERSHEY_SIMPLEX, 6, (230, 230, 250), 16)

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)

                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1               #rock

                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2             #paper

                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3              #scissors

                    ########
                    randomNumber = random.randint(1, 3)
                    imgAI = cv2.imread(f'Stuff/{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (295, 398))

                    #player score
                    if (playerMove == 1 and randomNumber == 3) or \
                        (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        scores[1] +=1
                        display = "You Won!"
                    #computer score
                    if (playerMove == 3 and randomNumber == 1) or \
                        (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1
                        display = "A.I. Won!"
                    if (playerMove == 1 and randomNumber == 1) or \
                        (playerMove == 2 and randomNumber == 2) or \
                            (playerMove == 3 and randomNumber == 3):
                        display = "IT'S A TIE"

                    print(playerMove)

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
