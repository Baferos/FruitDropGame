import ObjectClass
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from GameClass import Game
from GameParameters import *

# Initialize Camera
camera = cv2.VideoCapture(camera)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
detector = FaceMeshDetector(maxFaces=maxFaces)

# Initialize Game
game = Game()

# Initialize Object
game_object = ObjectClass.Object()


def print_score_lives():
    cv2.putText(img, f'Score: {game.get_score()}', (1000, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 128, 128), 3)
    cv2.putText(img, f'Lives: {game.get_lives()}', (1000, 150), cv2.FONT_HERSHEY_PLAIN, 3, (255, 128, 128), 3)


def is_object_near_the_mouth(detected_face, image):
    center_x, center_y = (detected_face[id_List_for_lips[0]][0] + detected_face[id_List_for_lips[1]][0]) / 2, \
                         (detected_face[id_List_for_lips[0]][1] + detected_face[id_List_for_lips[1]][1]) / 2

    half_width = objectWidth / 2
    half_height = objectHeight / 2
    distance = detector.findDistance((center_x, center_y), (game_object.get_position()[0] + half_width, \
                                                            game_object.get_position()[1] + half_height))[0]
    if debug_mode:
        p1 = (int(center_x), int(center_y))
        p2 = (int(game_object.get_position()[0] + half_width), int(game_object.get_position()[1] + half_height))
        cv2.line(image, p1, p2, (0, 255, 123), 3)
        print("Distance: ", distance)
    return distance < eatThreshold


def is_mouth_open(detected_face, image):
    up_down, _ = detector.findDistance(detected_face[id_List_for_lips[0]],
                                       detected_face[id_List_for_lips[1]])
    left_right, _ = detector.findDistance(detected_face[id_List_for_lips[2]],
                                          detected_face[id_List_for_lips[3]])
    ratio = int((up_down / left_right) * 100)
    if debug_mode:
        print("Mouth Ratio: ", ratio)
        if ratio > openThreshold:
            cv2.putText(image, "OPEN", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (128, 128, 128), 3)
        else:
            cv2.putText(image, "CLOSED", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (128, 128, 128), 3)
    return ratio > openThreshold


def eat_object(detected_face, image, cur_object):
    if is_object_near_the_mouth(detected_face, image) and is_mouth_open(detected_face, image):
        if game_object.get_is_eatable():
            game.increase_score()
        else:
            game.decrease_lives()

        if game.get_score() % lifeIncEvery == 0 and game.get_score() != 0:
            game.increase_lives()
        cur_object.new_object()


def check_if_game_over():
    # TODO: change this
    if game.get_lives() == 0:
        game.reset()


while True:
    success, img = camera.read()
    img, faces = detector.findFaceMesh(img, draw=False)

    img = cvzone.overlayPNG(img, game_object.get_object(), game_object.get_position())

    game_object.new_position(game.get_speed())

    if game_object.get_position()[1] > height - objectHeight:
        game_object.new_object()

    if faces:
        camera_face = faces[0]
        eat_object(camera_face, img, game_object)
        check_if_game_over()

    img = cv2.flip(img, 1)
    print_score_lives()

    cv2.imshow(title, img)
    key = cv2.waitKey(1)

    # Press q to exit
    if key == ord('q'):
        break
