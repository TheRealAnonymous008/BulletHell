import pygame
import time
import os
import math
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
        self.currTime = 0 
        pygame.sprite.Sprite.__init__(self)

    def setBirth(self, time):
        self.birth = time
    
    def getcurrTime(self, time):
        self.currTime =time

    def clearList(self):
        for k in self.shooter_list:
            self.shooter_list.remove(k)


# Make All Presets Here

class Preset1(Preset_Shooter):
    def __init__(self):
        Preset_Shooter.__init__(self)

        s = Shooter()
        s.setBirth(self.birth)
        s.setLocation(400, 0)
        s.setTarget(100, 600)
        s.setBulletParams(5, 5, 0 , 0)
        s.setShape(360, 20, 30)
        s.setIsSpinning(True)
        s.setBulletSize(7)
        
        p = Pattern(2)
        p.setParams([1, 10, 0, 0])
        s.setSpinPattern(p)
        s.setSpinRate(10)

        s.setROF(100)
        s.setIsAuto(True)
        s.setAmmo(300)
        self.shooter_list.add(s)

class Preset2(Preset_Shooter):
    def __init__(self):
        Preset_Shooter.__init__(self)
        mousex, mousey = pygame.mouse.get_pos()

        self.clearList()
        s = Shooter()
        s.setBirth(self.birth)
        s.setLocation(mousex,mousey)
        s.setColor(constants.red)
        s.setBulletParams(0,0, -10 , -10)
        s.setBulletsdeleteIfOut(False)
        s.setShape(360, 20, 0)
        s.setROF(100)
        s.setAmmo(1)
        s.setInRadius(200)

        self.shooter_list.add(s)

class Preset3(Preset_Shooter):
    def __init__(self):
        Preset_Shooter.__init__(self)
        mousex, mousey = pygame.mouse.get_pos()

        self.clearList()
        s = Shooter()
        s.setBirth(self.birth)
        s.setLocation(400, 0)
        s.setBulletParams(5, 5 , -0.5 , -0.5)
        s.setShape(60, 20, 0)
        s.setROF(100)
        s.setAmmo(100)
        s.setInRadius(100)
        s.setIsSpinning(True)
        s.setIsAuto(True)
        s.setSpinRate(100)

        self.shooter_list.add(s)


class Preset4(Preset_Shooter):
    def __init__(self):
        Preset_Shooter.__init__(self)
        self.clearList()
        s = Shooter()
        s.setMode(1)
        s.setColor(constants.yellow)
        s.setBirth(self.birth)
        s.setLocation(400, 0)
        s.setBulletParams(5, 5 , -0.5 , -0.5)
        s.setShape(360, 10, 0)
        s.setAmmo(1)
        s.setBulletLife(10)
        s.setLaserSpinRate(4)
        s.setIsSpinning(False)
        s.setIsAuto(True)

        self.shooter_list.add(s)


class Preset5(Preset_Shooter):
    def __init__(self):
        Preset_Shooter.__init__(self)
        self.clearList()
        s = Shooter()
        s.setMode(1)
        s.setColor(constants.red)
        s.setBirth(self.birth)
        s.setLocation(400, 300)
        s.setBulletParams(5, 5 , -0.5 , -0.5)
        s.setShape(360, 8, 0)
        s.setAmmo(1)
        s.setBulletLife(10)
        s.setSpinRate(10)
        s.setLaserSpinRate(4)
        s.setIsSpinning(True)
        s.setIsAuto(True)
        s.setBulletSize(10)
        s.setInRadius(100)

        self.shooter_list.add(s)

class Preset6(Preset_Shooter):
    def __init__(self):
        Preset_Shooter.__init__(self)
        self.clearList()
        s = Shooter()
        s.setColor(constants.cyan)
        s.setBirth(self.birth)
        s.setLocation(400, 300)
        s.setBulletParams(3, 3, 3 , 3)
        s.setShape(0, 1, 0)
        s.setAmmo(200)
        s.setBulletLife(10)
        s.setSpinRate(10)
        s.setIsSpinning(True)
        s.setIsAuto(True)
        s.setBulletsHoming(True)
        s.setBulletHomingDelay(200)
        s.setBulletHomingError(0.001)

        self.shooter_list.add(s)

class Preset7(Preset_Shooter):
    def __init__(self):
        Preset_Shooter.__init__(self)
        x =random.randint(0, constants.SWIDTH)
        y = random.randint(0, constants.SHEIGHT)
        self.clearList()
        s = Shooter()
        s.setColor(constants.yellow)
        s.setBirth(self.birth)
        s.setLocation(x, y)
        s.setBulletParams(2, 2 , -1 , -1)
        s.setShape(360, 20, 0)
        s.setAmmo(1)
        s.setBulletsSticky(True)
        s.setBulletsStickyTimer(1000)
        s.setBulletsStickyTimerStop(6000)
        s.setBulletsdeleteIfOut(False)
        s.setBulletsTargetting(True)

        self.shooter_list.add(s)

class Preset8(Preset_Shooter):
    def __init__(self):
        Preset_Shooter.__init__(self)
        self.clearList()
        s = Shooter()
        s.setColor(constants.magenta)
        s.setBirth(self.birth)
        s.setLocation(400, 300)
        s.setMode(2)
        s.setAmmo(10)
        s.setROF(500)
        s.setWaveArc(180)
        s.setWaveRadVel(10)
        s.setSpinRate(10)
        s.setIsSpinning(True)
        s.setWaveRadius(20)
        s.setShape(0, 1, 0)

        self.shooter_list.add(s)

        