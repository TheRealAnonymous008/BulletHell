import pygame
import time
import os
import math
import copy
import random
from entities import *
from constants import *
from shooter import *
from bullet import *


# The following file contains presets of shooters and shooting patterns

class Preset_Shooter(pygame.sprite.Sprite):
    def __init__(self):
        self.shooter_list =pygame.sprite.Group()
        self.birth = 0
        pygame.sprite.Sprite.__init__(self)

    def clearList(self):
        for k in self.shooter_list:
            self.shooter_list.remove(k)

    def setBirth(self, time):
        self.birth = time

class Preset1(Preset_Shooter):
    def __init__(self):
        Preset_Shooter.__init__(self)
        self.clearList()

    def prime(self):
        s = Shooter()
        s.setBulletParams(30, 30, 0 , 0)
        s.setShape(360, 10 , 0)
        s.setLocation(constants.SWIDTH / 2, constants.SHEIGHT / 2)
        s.setROF(300)
        s.setBulletsSinusoidal(30, 1)

        self.shooter_list.add(s)
        