import os
import random
import cv2

from GameParameters import width, objectWidth

# import images
folderFruits = 'Objects/eatable/'
folderNonEatable = 'Objects/non_eatable/'


class EatableNonEatable:
    is_eatable = False
    current_object = ''
    listFruits = os.listdir(folderFruits)
    listNonEatable = os.listdir(folderNonEatable)
    position = []
    fruits = []
    nonEatable = []

    # Constructor
    def __init__(self):
        for obj in self.listFruits:
            self.fruits.append(cv2.imread(f'{folderFruits}/{obj}', cv2.IMREAD_UNCHANGED))

        for obj in self.listNonEatable:
            self.nonEatable.append(cv2.imread(f'{folderNonEatable}/{obj}', cv2.IMREAD_UNCHANGED))
        self.new_object()

    def get_object(self):
        return self.current_object

    def get_is_eatable(self):
        return self.is_eatable

    def get_position(self):
        return self.position

    def set_position(self, x, y):
        self.position[0] = x
        self.position[1] = y

    def new_position(self, speed):
        self.position[1] += speed

    def new_object(self):
        fruit_or_non_eatable = random.randint(0, 1)
        if fruit_or_non_eatable == 0:
            self.is_eatable = True
            self.current_object = self.fruits[random.randint(0, len(self.fruits) - 1)]
        else:
            self.is_eatable = False
            self.current_object = self.nonEatable[random.randint(0, len(self.nonEatable) - 1)]

        self.position = [random.randint(objectWidth, (width - objectWidth)), 0]
