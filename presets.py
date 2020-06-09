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
        s = Shooter()
        b = 2
        s.setBirth(self.birth)
        s.setLocation(100, 100)
        s.setBulletColor(constants.red)
        s.setParams(3, b, 0, 0)
        s.setVisible(True)
        s.setROF(200)
        s.setAmmo(100)
        s.setShape(60, 3, 0)
        s.setBulletsTargetting(True)
        s.setBulletParams(3, 3, 0, 0)
        s.setTargettingError(10)
        s.setPolyMove(True)
        s.addVertex((constants.SWIDTH - 100, 100), 2000)
        s.addVertex((constants.SWIDTH - 100, constants.SHEIGHT - 100), 2000)
        s.addVertex((100, constants.SHEIGHT - 100), 2000)
        s.addVertex((100, 100), 2000)
        s.setPolyMoveLooping(True)
        s.fireWhenNotStop = True

        self.shooter_list.add(s)

        s = Shooter()

        s.setBirth(self.birth)
        s.setLocation(constants.SWIDTH - 100, 100)
        s.setVisible(True)

        s.setBulletColor(constants.red)
        s.setParams(3, b, 0, 0)
        s.setROF(200)
        s.setShape(60, 3, 0)
        s.setAmmo(100)
        s.setBulletsTargetting(True)
        s.setBulletParams(3, 3, 0, 0)
        s.setTargettingError(10)

        s.setPolyMove(True)
        
        s.addVertex((constants.SWIDTH - 100, constants.SHEIGHT - 100), 2000)
        s.addVertex((100, constants.SHEIGHT - 100) , 2000)
        s.addVertex((100, 100) , 2000)
        s.addVertex((constants.SWIDTH - 100, 100), 2000)
        s.setPolyMoveLooping(True)
        s.fireWhenNotStop = True
        self.shooter_list.add(s)

        s = Shooter()

        s.setBirth(self.birth)
        s.setLocation(100, constants.SHEIGHT - 100)
        s.setVisible(True)

        s.setBulletColor(constants.blue)
        s.setParams(3, b, 0, 0)
        s.setROF(200)
        s.setShape(60, 3, 0)
        s.setAmmo(100)
        s.setBulletsTargetting(True)
        s.setBulletParams(3, 3, 0, 0)
        s.setTargettingError(10)

        s.setPolyMove(True)
        
        s.addVertex((100, 100), 2000)
        s.addVertex((constants.SWIDTH - 100, 100), 2000)
        s.addVertex((constants.SWIDTH - 100, constants.SHEIGHT - 100), 2000)
        s.addVertex((100, constants.SHEIGHT - 100), 2000)
        s.setPolyMoveLooping(True)
        s.fireWhenNotStop = True
        
        self.shooter_list.add(s)
        s = Shooter()

        s.setBirth(self.birth)
        s.setLocation(constants.SWIDTH -100,constants.SHEIGHT -  100)
        s.setVisible(True)
        s.setBulletColor(constants.blue)
        s.setParams(3, b, 0, 0)
        s.setROF(200)
        s.setShape(60, 3, 0)
        s.setAmmo(100)
        s.setBulletsTargetting(True)
        s.setBulletParams(3, 3, 0, 0)
        s.setTargettingError(10)
        s.fireWhenNotStop = True 
        
        s.setPolyMove(True)
        
        s.addVertex((100, constants.SHEIGHT - 100), 2000)
        s.addVertex((100, 100), 2000)
        s.addVertex((constants.SWIDTH - 100, 100) , 2000)
        s.addVertex((constants.SWIDTH - 100, constants.SHEIGHT - 100), 2000)
        s.setPolyMoveLooping(True)
        self.shooter_list.add(s)

        # BREAK 

        s = Shooter()
        s.setBirth(self.birth)
        s.setLocation(100, 100)
        s.setBulletColor(constants.yellow)
        s.setParams(3, b, 0, 0)
        s.setVisible(True)
        s.setROF(503)
        s.setAmmo(40)
        s.setShape(360, 15, 0)
        s.setBulletParams(5, 5, -1, -1)
        s.setPolyMove(True)
        s.addVertex((constants.SWIDTH - 100, 100), 2000)
        s.addVertex((constants.SWIDTH - 100, constants.SHEIGHT - 100), 2000)
        s.addVertex((100, constants.SHEIGHT - 100), 2000)
        s.addVertex((100, 100), 2000)
        s.setPolyMoveLooping(True)
        s.fireWhenStop = True
        s.setBulletsTargetting(True)

        self.shooter_list.add(s)

        s = Shooter()

        s.setBirth(self.birth)
        s.setLocation(constants.SWIDTH - 100, 100)
        s.setVisible(True)

        s.setBulletColor(constants.yellow)
        s.setParams(3, b, 0, 0)
        s.setROF(503)
        s.setShape(360, 15, 0)
        s.setAmmo(40)
        s.setBulletParams(5, 5, -1, -1)

        s.setPolyMove(True)
        
        s.addVertex((constants.SWIDTH - 100, constants.SHEIGHT - 100), 2000)
        s.addVertex((100, constants.SHEIGHT - 100) , 2000)
        s.addVertex((100, 100) , 2000)
        s.addVertex((constants.SWIDTH - 100, 100), 2000)
        s.setPolyMoveLooping(True)
        s.fireWhenStop = True
        s.setBulletsTargetting(True)

        self.shooter_list.add(s)

        s = Shooter()

        s.setBirth(self.birth)
        s.setLocation(100, constants.SHEIGHT - 100)
        s.setVisible(True)

        s.setBulletColor(constants.green)
        s.setParams(3, b, 0, 0)
        s.setROF(503)
        s.setShape(360, 15, 0)
        s.setAmmo(40)
        s.setBulletParams(5, 5, -1, -1)
        s.setBulletsTargetting(True)

        s.setPolyMove(True)
        
        s.addVertex((100, 100), 2000)
        s.addVertex((constants.SWIDTH - 100, 100), 2000)
        s.addVertex((constants.SWIDTH - 100, constants.SHEIGHT - 100), 2000)
        s.addVertex((100, constants.SHEIGHT - 100), 2000)
        s.setPolyMoveLooping(True)
        s.fireWhenStop = True
        
        self.shooter_list.add(s)
        s = Shooter()

        s.setBirth(self.birth)
        s.setLocation(constants.SWIDTH -100,constants.SHEIGHT -  100)
        s.setVisible(True)
        s.setBulletColor(constants.green)
        s.setParams(3, b, 0, 0)
        s.setROF(503)
        s.setShape(360, 15, 0)
        s.setAmmo(40)
        s.setBulletParams(5, 5, -1, -1)
        s.setBulletsTargetting(True)
        s.fireWhenStop = True
        
        s.setPolyMove(True)
        
        s.addVertex((100, constants.SHEIGHT - 100), 2000)
        s.addVertex((100, 100), 2000)
        s.addVertex((constants.SWIDTH - 100, 100) , 2000)
        s.addVertex((constants.SWIDTH - 100, constants.SHEIGHT - 100), 2000)
        s.setPolyMoveLooping(True)
        self.shooter_list.add(s)

        # BREAK
 
        s = Shooter()
        s.setBirth(self.birth)
        s.setLocation(100, 100)
        s.setBulletColor(constants.cyan)
        s.setParams(3, b, 0, 0)
        s.setVisible(True)
        s.setROF(503)
        s.setAmmo(40)
        s.setShape(360, 15, 0)
        s.setBulletParams(5, 5, -1, -1)
        s.setPolyMove(True)
        s.addVertex((constants.SWIDTH - 100, 100), 2000)
        s.addVertex((constants.SWIDTH - 100, constants.SHEIGHT - 100), 2000)
        s.addVertex((100, constants.SHEIGHT - 100), 2000)
        s.addVertex((100, 100), 2000)
        s.setPolyMoveLooping(True)
        s.fireWhenStop = True
        s.setBulletsTargetting(True)
        
        s.setBulletsOrbit(True)
        s.setBulletOrbitParams(20, 0, 0)
        s.setBulletOrbitRadParams(5, -1)
        s.setBulletSize(5)

        self.shooter_list.add(s)

        s = Shooter()

        s.setBirth(self.birth)
        s.setLocation(constants.SWIDTH - 100, 100)
        s.setVisible(True)

        s.setBulletColor(constants.magenta)
        s.setParams(3, b, 0, 0)
        s.setROF(503)
        s.setShape(360, 15, 0)
        s.setAmmo(40)
        s.setBulletParams(5, 5, -1, -1)

        s.setPolyMove(True)
        
        s.addVertex((constants.SWIDTH - 100, constants.SHEIGHT - 100), 2000)
        s.addVertex((100, constants.SHEIGHT - 100) , 2000)
        s.addVertex((100, 100) , 2000)
        s.addVertex((constants.SWIDTH - 100, 100), 2000)
        s.setPolyMoveLooping(True)
        s.fireWhenStop = True
        s.setBulletsTargetting(True)
        
        s.setBulletsOrbit(True)
        s.setBulletOrbitParams(20, 0, 0)
        s.setBulletOrbitRadParams(5, -1)
        s.setBulletSize(5)

        self.shooter_list.add(s)

        s = Shooter()

        s.setBirth(self.birth)
        s.setLocation(100, constants.SHEIGHT - 100)
        s.setVisible(True)

        s.setBulletColor(constants.magenta)
        s.setParams(3, b, 0, 0)
        s.setROF(503)
        s.setShape(360, 15, 0)
        s.setAmmo(40)
        s.setBulletParams(5, 5, -1, -1)
        s.setBulletsTargetting(True)

        s.setPolyMove(True)
        
        s.addVertex((100, 100), 2000)
        s.addVertex((constants.SWIDTH - 100, 100), 2000)
        s.addVertex((constants.SWIDTH - 100, constants.SHEIGHT - 100), 2000)
        s.addVertex((100, constants.SHEIGHT - 100), 2000)
        s.setPolyMoveLooping(True)
        s.fireWhenStop = True
        
        s.setBulletsOrbit(True)
        s.setBulletOrbitParams(20, 0, 0)
        s.setBulletOrbitRadParams(5, -1)
        s.setBulletSize(5)

        self.shooter_list.add(s)
        s = Shooter()

        s.setBirth(self.birth)
        s.setLocation(constants.SWIDTH -100,constants.SHEIGHT -  100)
        s.setVisible(True)
        s.setBulletColor(constants.cyan)
        s.setParams(3, b, 0, 0)
        s.setROF(503)
        s.setShape(360, 15, 0)
        s.setAmmo(40)
        s.setBulletParams(5, 5, -1, -1)
        s.setBulletsTargetting(True)
        s.fireWhenStop = True
        
        s.setPolyMove(True)
        
        s.addVertex((100, constants.SHEIGHT - 100), 2000)
        s.addVertex((100, 100), 2000)
        s.addVertex((constants.SWIDTH - 100, 100) , 2000)
        s.addVertex((constants.SWIDTH - 100, constants.SHEIGHT - 100), 2000)
        s.setPolyMoveLooping(True)

        s.setBulletsOrbit(True)
        s.setBulletOrbitParams(20, 0, 0)
        s.setBulletOrbitRadParams(5, -1)
        s.setBulletSize(5)
        self.shooter_list.add(s)


class Preset2(Preset_Shooter):
    def __init__(self):
        Preset_Shooter.__init__(self)
        self.clearList()

    def prime(self):
        
        sizes = [25, 35, 45, 55]
        colors = [constants.red, constants.yellow, constants.green, constants.blue]
        accels = [2, 1.5, 1, 0.5]

        for i in range(0, 4):    
            s = Shooter()
            s.setBirth(self.birth)
            s.setLocation(SWIDTH / 2, 100)
            s.setVisible(True)
            s.setInRadius(sizes[i])
            s.setAmmo(10)
            s.setROF(700)
            s.setIsSpinning(True)
            s.setSpinRate(20)
            
            s.setBulletColor(colors[i])
            s.setBulletParams(2, 2, accels[i], accels[i])
            s.setShape(360, 30, 0)

            self.shooter_list.add(s)
            

