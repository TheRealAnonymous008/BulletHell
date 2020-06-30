import pygame
import time
import os
import math
import copy
import random
from patterns import *
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

# Make All Presets Here
class Preset1(Preset_Shooter):
    def __init__(self):
        Preset_Shooter.__init__(self)
        self.clearList()

    def prime(self):

        
        q = Shooter()
        q.setBulletParams(3, 3, 1, 1)
        q.setShape(360, 10, 0)
        q.setVisible(False)
        q.setROF(1000)
        q.setAmmo(2)

        p = Shooter()
        p.setBulletParams(3.5, 3.5, 0, 0)
        p.setShape(360, 10, 0)
        p.setVisible(False)
        p.setIsSpinning(True)
        p.setSpinRate(10)
        p.setROF(500)
        p.setAmmo(1)
        p.setMode(3)
        p.addShooter(q)
        p.setBulletColor(constants.red)


        r = Shooter()
        r.setBulletParams(-4, -4, -1, -1)
        r.setIsSpinning(True)
        r.setROF(100)
        r.setSpinRate(10)
        r.setAmmo(40)
        r.setBulletColor(constants.blue)
        r.setShape(0, 1, 0)

        s = Shooter()
        s.setMode(3)
        s.setLocation(constants.SWIDTH / 2, constants.SHEIGHT/2 )
        s.setBulletsOrbit(True)
        s.setBulletOrbitParams(30, 0, 100)
        s.setROF(6000)
        s.setAmmo(4)
        s.addShooter(p)
        s.addShooter(r)
        s.setShape(360, 5, 0)
        s.setBulletColor(constants.black)
        self.shooter_list.add(s)
        
        s = Shooter()
        s.setMode(3)
        s.setLocation(constants.SWIDTH / 2, constants.SHEIGHT/2 )
        s.setBulletsOrbit(True)
        s.setBulletOrbitParams(-30, 0, 100)
        s.setROF(6000)
        s.setAmmo(1)
        s.addShooter(r)
        s.setShape(360, 5, 0)
        s.setBulletColor(constants.black)
        self.shooter_list.add(s)

        s = Shooter()
        s.setLocation(constants.SWIDTH / 2, constants.SHEIGHT / 2)
        s.setBulletParams(5, 5, 0, 0)
        s.setShape(360, 15, 0)
        s.setIsOscillating(True)
        s.setOscillationBounds(0,360)
        s.setROF(150)
        s.setAmmo(30)
        s.setSpinRate(10)
        s.setBulletColor(constants.yellow)
        self.shooter_list.add(s)

class Preset2(Preset_Shooter):
    def __init__(self):
        Preset_Shooter.__init__(self)
        self.clearList()

    def prime(self):
        s = Shooter()
        s.setLocation(constants.SWIDTH / 2 - 250, 50)
        s.setBulletParams(5, 5, 0, 0)
        s.setBulletsTargetting(True)
        s.setSpinRate(10)
        s.setROF(500)
        s.setAmmo(10)
        s.setShape(0, 1, 0)
        s.setOscillationBounds(0, 360)
        s.setBurstParams(10, 50)
        self.shooter_list.add(s)