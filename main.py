import os
import random

import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector

# Game Parameters
width = 1280
height = 720
openThreshold = 65
eatThreshold = 70

debug = False

# import images
folderFruits = 'Objects/eatable/'
folderNonEatable = 'Objects/non_eatable/'

listFruits = os.listdir(folderFruits)
fruits = []
for obj in listFruits:
    fruits.append(cv2.imread(f'{folderFruits}/{obj}', cv2.IMREAD_UNCHANGED))

listNonEatable = os.listdir(folderNonEatable)
nonEatable = []
for obj in listNonEatable:
    nonEatable.append(cv2.imread(f'{folderNonEatable}/{obj}', cv2.IMREAD_UNCHANGED))

# Initialize Camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
detector = FaceMeshDetector(maxFaces=1)

idList = [0, 17, 78, 292]

currentObject = fruits[0]
position = [300, 0]
score = 0
lives = 3
speed = 5

global isEatable


def reset_object():
    global isEatable
    fruit_or_non_eatable = random.randint(0, 1)
    if fruit_or_non_eatable == 0:
        isEatable = True
        current_object = fruits[random.randint(0, len(fruits) - 1)]
    else:
        isEatable = False
        current_object = nonEatable[random.randint(0, len(nonEatable) - 1)]
    position[0] = random.randint(100, 1180)
    position[1] = 0
    return current_object


def init_game():
    global currentObject, position, score, lives
    currentObject = reset_object()
    score = 0
    lives = 3


init_game()
while True:
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)

    img = cvzone.overlayPNG(img, currentObject, position)

    position[1] += speed
    if position[1] > height - 100 - 50:
        currentObject = reset_object()

    if faces:
        face = faces[0]
        if debug:
            for idNo, point in enumerate(face):
                cv2.putText(img, str(idNo), point, cv2.FONT_HERSHEY_PLAIN, 0.67, (255, 0, 123), 1)

        if debug:
            for point_id in idList:
                cv2.circle(img, face[point_id], 5, (255, 0, 123), 5)
            cv2.line(img, face[idList[0]], face[idList[1]], (255, 0, 123), 3)
            cv2.line(img, face[idList[2]], face[idList[3]], (255, 0, 123), 3)

        upDown, _ = detector.findDistance(face[idList[0]], face[idList[1]])
        leftRight, _ = detector.findDistance(face[idList[2]], face[idList[3]])
        # Distance between mouth and object
        cx, cy = (face[idList[0]][0] + face[idList[1]][0]) // 2, (face[idList[0]][1] + face[idList[1]][1]) // 2
        if debug:
            cv2.line(img, (cx, cy), (position[0] + 50, position[1] + 50), (0, 255, 123), 3)

        mouth_distance = detector.findDistance((cx, cy), (position[0] + 50, position[1] + 50))[0]

        # open/close mouth
        ratio = int((upDown / leftRight) * 100)
        if debug:
            print("Mouth Ratio: ", ratio)
            if ratio > openThreshold:
                cv2.putText(img, "OPEN", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
            else:
                cv2.putText(img, "CLOSED", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

        if mouth_distance < eatThreshold:
            if ratio > openThreshold:
                currentObject = reset_object()
                if isEatable:
                    score += 1
                else:
                    lives -= 1

                if score % 5 == 0 and score != 0:
                    lives += 1

        if lives == 0:
            init_game()

    img = cv2.flip(img, 1)

    cv2.putText(img, f'Score: {score}', (1000, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 128, 128), 3)
    cv2.putText(img, f'Lives: {lives}', (1000, 150), cv2.FONT_HERSHEY_PLAIN, 3, (255, 128, 128), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
