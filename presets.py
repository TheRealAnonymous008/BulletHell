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
        s.setBulletParams(50, 50, 0 ,0)
        s.setShape(360, 6 , 30, True, 4)
        s.setLocation(400, 300)
        s.setROF(500)
        s.setBulletOrbitParams(10, 0, 100, 40)
        s.setAmmo(1)
        s.setBulletsSinusoidal(100)
        self.shooter_list.add(s)

        
        