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

        r = Shooter()
        r.setShape(0, 1, 0)
        r.setSpinParams(30)
        r.setLocation(constants.SWIDTH / 2, constants.SHEIGHT / 2)
        r.setMode(3)
        r.setROF(5000)

        s = Shooter()
        s.setROF(1000)
        s.setShape(360, 6, 0)
        s.setSpinParams(6)
        s.setBulletParams(50, 50 , -2.5,  -2.5)
        s.setBurstParams(10, 100)
        s.setAmmo(1)
        r.addShooter(s)
        
        s = Shooter()
        s.setROF(1000)
        s.setShape(360, 6, 0)
        s.setSpinParams(-6)
        s.setBulletParams(50, 50, -2.5, -2.5)
        s.setBurstParams(10, 100)
        s.setAmmo(1)
        r.addShooter(s)
        
        self.shooter_list.add(r)

        p = Shooter()
        p.setLocation(constants.SWIDTH / 2, constants.SHEIGHT / 2)
        p.setBulletsOrbit(True)
        p.setROF(100)
        p.setBulletOrbitParams(90, 0, 100)
        p.setAmmo(1)
        p.setShape(0, 1, 0)
        self.shooter_list.add(p)