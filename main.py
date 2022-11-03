import os
import random

import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector

#Game Parameters
width = 1280
height = 720
openThreshold = 65

# import images
folderFruits = 'Objects/eatable/'
folderNonEatable = 'Objects/noneatable/'

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
speed = 5

def resetObject():
    FruitOrNonEatable = random.randint(0, 1)
    if FruitOrNonEatable == 0:
        currentObject = fruits[random.randint(0, len(fruits) - 1)]
    else:
        currentObject = nonEatable[random.randint(0, len(nonEatable) - 1)]
    position[0] =random.randint(100, 1180)
    position[1] = 0
    return currentObject

def initGame():
    global currentObject, position, score, lives
    currentObject = resetObject()
    score = 0
    lives = 3

initGame()
while True:
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)

    img = cvzone.overlayPNG(img, currentObject, position)

    position[1] += speed
    if position[1] > height - 100 - 50:
        currentObject = resetObject()


    if faces:
        face = faces[0]
        # for idNo, point in enumerate(face):
        #     cv2.putText(img, str(idNo), point, cv2.FONT_HERSHEY_PLAIN, 0.67, (255, 0, 123), 1)
        for id in idList:
            cv2.circle(img, face[id], 5, (255, 0, 123), 5)
        cv2.line(img, face[idList[0]], face[idList[1]], (255, 0, 123), 3)
        cv2.line(img, face[idList[2]], face[idList[3]], (255, 0, 123), 3)

        upDown, _ = detector.findDistance(face[idList[0]], face[idList[1]])
        leftRight, _ = detector.findDistance(face[idList[2]], face[idList[3]])
        ratio = int((upDown / leftRight) * 100)
        print(ratio)

        if ratio > openThreshold:
            cv2.putText(img, "OPEN", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        else:
            cv2.putText(img, "CLOSED", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)


    cv2.imshow("Image", img)
    cv2.waitKey(1)
