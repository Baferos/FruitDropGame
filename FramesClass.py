import cv2
from EatableNonEatableClass import EatableNonEatable
from GameRulesClass import GameRules
from cvzone.FaceMeshModule import FaceMeshDetector
from GameParameters import *
import cvzone


class Frames(object):
    camera = cv2.VideoCapture(0)

    def __init__(self, frame_width, frame_height):

        self.camera = cv2.VideoCapture(DefaultCamera)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
        self.detector = FaceMeshDetector(maxFaces=maxFaces)
        self.success, self.img = self.camera.read()
        self.faces = None
        self.face = None

        # Initialize Game
        self.game_rules = GameRules()
        # Initialize eatable or non-eatable object
        self.eatable_non_eatable = EatableNonEatable()

    def update_frame(self):
        self.success, self.img = self.camera.read()

    def get_face(self):
        self.img, self.faces = self.detector.findFaceMesh(self.img,  draw=True if debug_mode else False)
        if self.faces:
            self.face = self.faces[0]

    def print_score_lives(self):
        cv2.putText(self.img, f'Score: {self.game_rules.get_score()}', (1000, 100), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 128, 128), 3)
        cv2.putText(self.img, f'Lives: {self.game_rules.get_lives()}', (1000, 150), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 128, 128), 3)

    def print_game_over(self):
        cv2.putText(self.img, "Game Over", (300, 400), cv2.FONT_HERSHEY_PLAIN, 7, (255, 0, 255), 10)
        cv2.putText(self.img, 'Press space to restart', (300, 400 + 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 128, 128), 3)
        cv2.putText(self.img, 'Press "q" to quit', (300, 400 + 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 128, 128), 3)

    def is_mouth_open(self):
        up_down, _ = self.detector.findDistance(self.face[id_List_for_lips[0]],
                                                self.face[id_List_for_lips[1]])
        left_right, _ = self.detector.findDistance(self.face[id_List_for_lips[2]],
                                                   self.face[id_List_for_lips[3]])
        ratio = int((up_down / left_right) * 100)
        if debug_mode:
            print("Mouth Ratio: ", ratio)
            if ratio > openThreshold:
                cv2.putText(self.img, "OPEN", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (128, 128, 128), 3)
            else:
                cv2.putText(self.img, "CLOSED", (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (128, 128, 128), 3)
        return ratio > openThreshold

    def is_object_near_the_mouth(self):
        center_x, center_y = (self.face[id_List_for_lips[0]][0] + self.face[id_List_for_lips[1]][0]) / 2, \
                             (self.face[id_List_for_lips[0]][1] + self.face[id_List_for_lips[1]][1]) / 2

        half_width = objectWidth / 2
        half_height = objectHeight / 2
        eatable_non_eatable_x, eatable_non_eatable_y = self.eatable_non_eatable.get_position()[0], \
                                                       self.eatable_non_eatable.get_position()[1]

        distance = self.detector.findDistance((center_x, center_y),
                                              (eatable_non_eatable_x + half_width, \
                                               eatable_non_eatable_y + half_height))[0]
        if debug_mode:
            p1 = (int(center_x), int(center_y))
            p2 = (int(eatable_non_eatable_x + half_width), int(eatable_non_eatable_y + half_height))
            cv2.line(self.img, p1, p2, (0, 255, 123), 3)
            print("Distance: ", distance)
        return distance < eatThreshold

    def check_eat_object(self):
        if self.is_object_near_the_mouth() and self.is_mouth_open():
            if self.eatable_non_eatable.get_is_eatable():
                self.game_rules.increase_score()
                if self.game_rules.get_score() % lifeIncEvery == 0 and self.game_rules.get_score() != 0:
                    self.game_rules.increase_speed()
                    self.game_rules.increase_lives()
            else:
                self.game_rules.decrease_lives()

            self.eatable_non_eatable.new_object()


    def game_loop(self):
        while True:
            self.update_frame()
            self.get_face()
            if not self.game_rules.check_if_game_over():
                self.img = cvzone.overlayPNG(self.img, self.eatable_non_eatable.get_object(),
                                             self.eatable_non_eatable.get_position())
                self.eatable_non_eatable.new_position(self.game_rules.get_speed())
                # Reset eatable or non-eatable object if it is out of the frame
                if self.eatable_non_eatable.get_position()[1] > height - objectHeight:
                    self.eatable_non_eatable.new_object()

                if self.face is not None:
                    self.check_eat_object()

            # flip the frame
            self.img = cv2.flip(self.img, 1)

            if not self.game_rules.check_if_game_over():
                # print score and lives
                self.print_score_lives()
            else:
                self.print_game_over()

            # show the frame
            cv2.imshow(title, self.img)

            print("speed: ", self.game_rules.get_speed())
            # wait for a key press
            key = cv2.waitKey(1)

            # Press q to exit
            if key == ord('q'):
                break
            if key == ord(' '):
                self.game_rules.reset()
