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
        s.setShape(360, 10, 0)
        s.setROF(300)
        s.setAmmo(1)
        s.setLocation(150, 300)
        s.setBulletParams(50, 50, 1, 1)
        s.setBulletsHoming(True, 1000, 3000, None, 0, False)
        self.shooter_list.add(s)
