import ObjectClass
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from GameClass import Game
from GameParameters import *

# Initialize Camera
cap = cv2.VideoCapture(camera)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
detector = FaceMeshDetector(maxFaces=maxFaces)

# Initialize Game
game = Game()

# Initialize Object
game_object = ObjectClass.Object()

while True:
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw=False)

    img = cvzone.overlayPNG(img, game_object.get_object(), game_object.get_position())

    game_object.new_position(game.get_speed())

    if game_object.get_position()[1] > height - objectHeight:
        currentObject = game_object.new_object()

    if faces:
        face = faces[0]
        if debug_mode:
            for idNo, point in enumerate(face):
                cv2.putText(img, str(idNo), point, cv2.FONT_HERSHEY_PLAIN, 0.67, (255, 0, 123), 1)

        if debug_mode:
            for point_id in id_List_for_lips:
                cv2.circle(img, face[point_id], 5, (255, 0, 123), 5)
            cv2.line(img, face[id_List_for_lips[0]], face[id_List_for_lips[1]],
                     (255, 0, 123), 3)
            cv2.line(img, face[id_List_for_lips[2]], face[id_List_for_lips[3]],
                     (255, 0, 123), 3)

        upDown, _ = detector.findDistance(face[id_List_for_lips[0]],
                                          face[id_List_for_lips[1]])
        leftRight, _ = detector.findDistance(face[id_List_for_lips[2]],
                                             face[id_List_for_lips[3]])
        # Distance between mouth and object
        cx, cy = (face[id_List_for_lips[0]][0] + face[id_List_for_lips[1]][0]) // 2, (
                face[id_List_for_lips[0]][1] + face[id_List_for_lips[1]][1]) // 2
        if debug_mode:
            cv2.line(img, (cx, cy), (game_object.get_position()[0] + 50, game_object.get_position()[1] + 50),
                     (0, 255, 123), 3)

        mouth_distance = \
        detector.findDistance((cx, cy), (game_object.get_position()[0] + 50, game_object.get_position()[1] + 50))[0]

        # open/close mouth
        ratio = int((upDown / leftRight) * 100)
        if debug_mode:
            print("Mouth Ratio: ", ratio)
            if ratio > openThreshold:
                cv2.putText(img, "OPEN", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
            else:
                cv2.putText(img, "CLOSED", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)

        if mouth_distance < eatThreshold:
            if ratio > openThreshold:
                if game_object.get_is_eatable():
                    game.increase_score()
                else:
                    game.decrease_lives()

                if game.get_score() % 5 == 0 and game.get_score() != 0:
                    game.increase_lives()
                currentObject = game_object.new_object()

        if game.get_lives() == 0:
            game.reset()

    img = cv2.flip(img, 1)

    cv2.putText(img, f'Score: {game.get_score()}', (1000, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 128, 128), 3)
    cv2.putText(img, f'Lives: {game.get_lives()}', (1000, 150), cv2.FONT_HERSHEY_PLAIN, 3, (255, 128, 128), 3)

    cv2.imshow("made by Ilias Baferos", img)
    cv2.waitKey(1)
