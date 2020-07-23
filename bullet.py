import pygame
import math
import constants
from entities import *

SWIDTH = constants.SWIDTH
SHEIGHT = constants.SHEIGHT
OFFSET = constants.OFFSET
FPS = constants.FPS
defsize = constants.default_bullet_size

# Rules:
# 0 -> delete if out of bounds
# 1 -> 

class Bullet(Entity):

    def __init__ (self):
        self.size = defsize
        self.color = constants.white
        
        # rules
        self.deleteIfOut = True
        self.homing = False

        Entity.__init__(self)

    def setBirth(self, val):
        self.birth = val

    def setHoming(self, val):
        self.homing = val

    def setdeleteIfOut(self, val):
        self.deleteIfOut = val

    # Number of ticks before bullet disappears

    def setLife(self, life):
        self.life = life

    def setColor(self, color):
        self.color = color 

    def setSize(self, size):
        self.size = size

    def draw(self, screen, time):
        x = int(self.xpos)
        y = int(self.ypos)

        size = self.size
        if(x - size <-1* OFFSET or y - size < -1 * OFFSET or x + size > SWIDTH + OFFSET or y + size > SHEIGHT + OFFSET):
            self.motion(time)
            return

        else:
            pygame.draw.circle(screen, self.color, (x, y), self.size)
            self.motion(time)
            

class Laser(Bullet):

    # Laser Thickness is set through Size

    def __init__ (self):
        self.length = 8000
        self.angle = 0
        self.laserspinRate = 0
        Bullet.__init__(self)

    def setAngle(self, angle):
        self.angle = angle

    def setLaserSpinRate(self, spinrate):
        self.laserspinRate = spinrate / 1000

    def setLength(self, length):
        self.length = length 

    def draw(self, screen, time ):
        x = int(self.xpos) 
        y = int(self.ypos)
        targetx = self.length * math.cos(self.angle)
        targety = self.length * math.sin(self.angle)
        pygame.draw.line(screen, self.color, (x, y), (targetx, targety), self.size)
        self.motion()

    def motion(self):
        mousex, mousey = pygame.mouse.get_pos()
        target = 0
        angle = math.atan2((mousey - self.ypos), (mousex - self.xpos))

        self.angle += self.laserspinRate

class Wave(Bullet):

    def __init__(self):
        self.centerx = 0
        self.centery = 0
        self.arc = math.radians(360)
        self.radius = 0
        self.rotation = 0
        self.radvel = 10
        Bullet.__init__(self)

    def setWaveParams(self, centerx, centery, arc, radius, radvel, rotation):
        self.centerx = centerx
        self.centery = centery
        self.arc = math.radians(arc)
        self.radius = radius
        self.rotation = rotation
        self.radvel = radvel

    def draw(self, screen, time):
        if self.arc != math.radians(360):
            pygame.draw.arc(screen, self.color, (self.centerx - self.radius, self. centery - self.radius, 2 * self.radius, 2*  self.radius), self.rotation, self.rotation + self.arc, self.size)
        else:
            pygame.draw.circle(screen, self.color, (int(self.centerx), int(self.centery)), int(self.radius), self.size)

        self.motion()

    def motion(self):
        self.radius += self.radvel

